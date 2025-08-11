---
permalink: /scratch_tp
---

{% for scratch_tp in site.scratch_tp %}
  <h2>
    <a href="{{ scratch_tp.url }}">
      {{ scratch_tp.name }} - {{ scratch_tp.position }}
    </a>
  </h2>
{% endfor %}