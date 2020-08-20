![alt text](https://upload.wikimedia.org/wikipedia/commons/5/55/Phantom_Unit_Logo.jpg)

# {{nombre}}

> Trabajo {{trabajo}} - {{email}}

{% for job in jobs %}
### :open_file_folder: {{job.nombre}} - {{job.anio}}

### :heavy_check_mark: {{job.puesto}}
*{{job.descripcion}}*
{% endfor %}
