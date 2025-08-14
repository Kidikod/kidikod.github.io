# kidikod.github.io

# Récupération du code
Le dépôt utilise collection sous forme de submodules :
- _scratch_tp : correspond au dépôt scratch_tp contenant tous les ateliers scratchs.

Aussi, la récupération du code source doit inclure les submodules avec cette commande.

```
git clone --recurse-sumodules https://github.com/Kidikod/kidikod.github.io.git
```

Si c'est déjà cloné, on peut toujours récupérer les submodules en lancant cette commande.


```
git submodule update --init
```

Pour l'écriture de block scratch en français, ce référer à la doc :
https://patrice-hardouin.canoprof.fr/eleve/Technologie%203e/Travaux_algorithmique_corrige/res/main.pdf

RAF :
- Tester la génération de PDF avec pandoc
- Trouver un moyen pour utiliser le pst-write hook avec githubpage (mais visiblement, il faudra faire la génération de site manuellement avec les github action)
- Ou alors utiliser un github action ou un githook pour lancer la génération de pdf à ajouter dans le dépot
