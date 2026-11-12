<!-- logo:start -->
<!-- logo:end -->

**Français** · [English](readme.en.md)

# Disk Info

<!-- version:auto -->
**Version : 1.0.0**
<!-- /version:auto -->

Petit service Kodi qui publie l'**espace disque de la partition de données** pour
les skins. Kodi ne mesure que `/` : sur **CoreELEC / LibreELEC**, c'est l'image
système en lecture seule (`loop0`), toujours pleine à 100 %. Ce service mesure la
partition qui contient le dossier de Kodi (`/storage` sur CoreELEC) et la rend
lisible par le skin.

Conçu pour le skin **Arctic: Worms**, utilisable par n'importe quel skin. Pour
Kodi 19 « Matrix » et suivants.

- **Dépôt** : `github.com/TheWorms/kodi-addon-diskinfo`
- **Identifiant Kodi** : `service.worms.diskinfo`
- **Nom affiché** : Disk Info · **Licence** : MIT

---

## Ce qu'il fait

Au démarrage de Kodi puis à intervalle régulier (60 s par défaut), le service lit
l'espace de la partition et le publie en propriétés de la fenêtre d'accueil :

| Propriété | Exemple | Contenu |
|---|---|---|
| `Window(Home).Property(DiskInfo.UsedPercent)` | `25` | pourcentage utilisé, calculé comme `df` |
| `Window(Home).Property(DiskInfo.FreePercent)` | `75` | pourcentage libre |
| `Window(Home).Property(DiskInfo.Total)` | `32 GB` | taille de la partition |
| `Window(Home).Property(DiskInfo.Used)` | `8.0 GB` | espace utilisé |
| `Window(Home).Property(DiskInfo.Free)` | `24 GB` | espace disponible |
| `Window(Home).Property(DiskInfo.Path)` | `/storage/.kodi/` | dossier mesuré |

Il n'a pas d'interface : rien ne s'affiche tant que le skin ne lit pas ces
propriétés. **Arctic: Worms** les affiche dans la tuile **Stockage** des infos
système et retombe sur la valeur de Kodi quand le service est absent.

Pour l'utiliser dans un autre skin, par exemple :

```xml
<label>$INFO[Window(Home).Property(DiskInfo.UsedPercent)] % utilisés sur $INFO[Window(Home).Property(DiskInfo.Total)]</label>
```

## Installer

### Via le dépôt TheWorms (recommandé, mises à jour automatiques)

1. Installe le dépôt :
   `https://raw.githubusercontent.com/TheWorms/kodi-repo/main/zips/repository.theworms/repository.theworms.zip`
2. Add-ons → **Installer depuis un dépôt** → *TheWorms Repository* → *Services* →
   **Disk Info** → Installer.

### Manuelle (zip)

1. Récupère `service.worms.diskinfo-x.y.z.zip`.
2. Système → Add-ons → active **Sources inconnues**.
3. Add-ons → **Installer depuis un fichier zip**.

Le service démarre aussitôt, sans redémarrer Kodi.

## Réglages

| Réglage | Défaut | Description |
|---|---|---|
| Dossier à mesurer | vide | Vide : la partition du dossier de Kodi (`/storage` sur CoreELEC). Sinon, un dossier au choix (disque USB, NAS monté…) |
| Intervalle de rafraîchissement | 60 s | Fréquence de relecture (10 à 600 s) |

## Dépannage

- **Le skin affiche toujours 100 %** : vérifie que le service est activé, puis en
  SSH :
  ```bash
  grep worms.diskinfo /storage/.kodi/temp/kodi.log
  ```
  Une ligne `/storage/.kodi/ : … utilisés sur … (… %)` confirme la mesure. Si elle
  est là, c'est le skin qui ne lit pas les propriétés.
- **« lecture impossible » dans le journal** : le dossier choisi dans les réglages
  n'existe pas ou n'est pas monté. Le service revient au dossier de Kodi.

## Licence

MIT — voir `LICENSE.txt`.
