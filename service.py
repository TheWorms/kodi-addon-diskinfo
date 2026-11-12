# -*- coding: utf-8 -*-
"""Publie l'espace disque de la partition de données en propriétés de la fenêtre d'accueil."""
import os

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

HOME = 10000
PREFIX = 'DiskInfo.'
KEYS = ('UsedPercent', 'FreePercent', 'Total', 'Used', 'Free', 'Path')


def log(msg, level=xbmc.LOGINFO):
    xbmc.log('[service.worms.diskinfo] %s' % msg, level)


def human(n):
    """Taille lisible : 512 MB, 14.2 GB, 1.82 TB (unités binaires, comme df -h)."""
    n = float(n) / (1024 * 1024)
    if n < 1024:
        return '%d MB' % round(n)
    n /= 1024
    if n < 1024:
        return ('%.1f GB' % n) if n < 100 else ('%d GB' % round(n))
    return '%.2f TB' % (n / 1024)


def settings():
    addon = xbmcaddon.Addon()  # instance fraîche : reflète les réglages modifiés
    path = addon.getSetting('path').strip()
    try:
        interval = int(addon.getSetting('interval') or 60)
    except ValueError:
        interval = 60
    return path, max(10, interval)


def target(path):
    if path:
        path = xbmcvfs.translatePath(path)
        if os.path.isdir(path):
            return path
    return xbmcvfs.translatePath('special://home/')


def measure(path):
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    if total <= 0:
        raise OSError('taille nulle pour %s' % path)
    # même calcul que df : utilisé / (utilisé + disponible), arrondi au-dessus
    denom = used + free
    pct = int(-(-used * 100 // denom)) if denom > 0 else 0
    return {
        'UsedPercent': str(pct),
        'FreePercent': str(100 - pct),
        'Total': human(total),
        'Used': human(used),
        'Free': human(free),
        'Path': path,
    }


def clear(win):
    for key in KEYS:
        win.clearProperty(PREFIX + key)


def main():
    monitor = xbmc.Monitor()
    win = xbmcgui.Window(HOME)
    last = None
    failed = False
    while not monitor.abortRequested():
        path, interval = settings()
        try:
            values = measure(target(path))
            failed = False
        except (OSError, AttributeError) as exc:
            values = None
            if not failed:
                log('lecture impossible : %s' % exc, xbmc.LOGWARNING)
                failed = True
        if values != last:
            if values:
                for key in KEYS:
                    win.setProperty(PREFIX + key, values[key])
                if last is None or values['Path'] != last.get('Path'):
                    log('%s : %s utilisés sur %s (%s %%)' % (
                        values['Path'], values['Used'], values['Total'], values['UsedPercent']))
            else:
                clear(win)
            last = values
        if monitor.waitForAbort(interval):
            break
    clear(win)


if __name__ == '__main__':
    main()
