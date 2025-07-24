---
title:  "Un article"
date:   2025-07-21 23:25:29 +0000
categories: test
page_js:
  - /assets/js/scratchblocks.min.js
  - /assets/js/translations-all.js
---
Ceci est un article rédigé dans un dossier séparé pour voir s'il sera tout de même généré par jekyll

<pre class="blocks">
quand le drapeau vert pressé
avancer de (10) pas
</pre>

un petit texte d'explication avec un bloc <code class="b">(abscisse x)</code> en plein milieu.

<script>
scratchblocks.renderMatching('pre.blocks', {
  style:     'scratch3',
  languages: ['fr'],
  scale: 1,
});
scratchblocks.renderMatching("code.b", {
  inline: true,
  style:     'scratch3',
  languages: ['fr'],
  scale: 0.75,
});
</script>