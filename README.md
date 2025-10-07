# kidikod.github.io

Pour l'écriture de block scratch en français, ce référer à la doc :
https://patrice-hardouin.canoprof.fr/eleve/Technologie%203e/Travaux_algorithmique_corrige/res/main.pdf

RAF :
- Tester la génération de PDF avec pandoc
- Trouver un moyen pour utiliser le pst-write hook avec githubpage (mais visiblement, il faudra faire la génération de site manuellement avec les github action)
- Ou alors utiliser un github action ou un githook pour lancer la génération de pdf à ajouter dans le dépot

- git clone <le projet>
- cd kidikod.github.io
- git submodule update --remote --init --recursive

Pour pouvoir travailler sur scratch_tp depuis kidikod.github.io
- cd _scratch_tp
- git switch main

Pour pousser les modifications dans _scratch_tp depuis kidikod.github.io
- cd _scratch_tp
- git add .
- git commit -m "un message de commit"
- cd ..
- git add _scratch_tp
- git commit -m "mise à jour du submodule _scratch_tp"
- git push --recurse-submodules=on-demand 
