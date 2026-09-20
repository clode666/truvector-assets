# truvector-assets

Médias déportés de **TRUvector.dev** (musique, galerie), servis via le CDN **jsDelivr**.

```
musique/   # 12 MP3
galerie/   # images .webp (affichage) + .png (HD)
```

## Utilisation
Dépôt **public** GitHub `clode666/truvector-assets`. Les fichiers sont servis par :

`https://cdn.jsdelivr.net/gh/clode666/truvector-assets@main/<chemin>`

Le site principal pointe ici via `assets/js/assets.js` (variable `TRU_ASSET_BASE`).

### Mettre à jour un média
1. Remplace le fichier ici et `git push`.
2. jsDelivr met en cache `@main` ~24 h–7 j. Pour forcer : purge `https://purge.jsdelivr.net/gh/clode666/truvector-assets@main/<chemin>` ou crée un tag (ex. `v1`) et pointe `TRU_ASSET_BASE` sur `@v1`.
