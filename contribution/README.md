## Issue #2150: Document that `Control` can be used to implement new Leaflet plugins

> The Control class can be used to implement new leaflet plugins in user code (e.g. without creating adding a new plugin class itself). This needs to be documented.

---

## Proposed Documentation: Using `Control` for Custom Controls / Plugins

Folium provides a generic `Control` class (in `folium.features.Control`) which can be used by users to add new custom Leaflet controls directly from their own code, without modifying Folium core or writing a full plugin class. I have added this solution in docs/user_guids/plugins.rst.

Below is a short guide and minimal example of how to use it.

### How it works (steps)

1. **Import and subclass (or instantiate) `Control`**  
   Use `from folium.features import Control`.

2. **Override or provide a Jinja2 template for the control’s JS**  
   Define a `self._template` with a macro that produces the necessary Leaflet JS (for example defining `onAdd`) to create your UI element.

3. **Add the control to a map**  
   Use `.add_to(map)` so that when rendering, your custom control’s JS is included.

4. (Optional) **Document and test it**  
   In Folium’s docs, include this pattern under “Custom Controls / Plugins” with example code. Add tests or examples to the examples folder.

### Example

Here’s a minimal working example you might include in docs or in user code:

```python
import jinja2
import folium
from folium.features import Control

class MyButtonControl(Control):
    def __init__(self, text: str, position: str = "topright"):
        super().__init__(position=position)
        self.text = text

    def render(self, **kwargs):
        # define the JS template for the control
        self._template = jinja2.Template("""
        {% macro script(this, kwargs) %}
        L.Control.extend({
            onAdd: function(map) {
                var btn = L.DomUtil.create('button');
                btn.innerHTML = '{{ this.text }}';
                btn.onclick = function() {
                  alert('Button clicked: {{ this.text }}');
                };
                return btn;
            }
        });
        new (L.Control.extend)({ position: '{{ this.position }}' }).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)
        super().render(**kwargs)

# Usage:
m = folium.Map(location=[0, 0], zoom_start=2)
MyButtonControl("Click me", position="topright").add_to(m)
m.save("map_with_button.html")
```


### The draft pull request for the updates I made:
[Pull Request Screen Shot](pr.png)

