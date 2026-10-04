"""
Modular Arithmetic Grid — 2D linear congruence table.

Renders an N x N grid where cell (x, y) holds the value of
    (x * A + y * B) mod N

as an HTML5 canvas, suitable for display in a Jupyter/IPython notebook.
Each row/column represents one residue class mod N; the resulting
pattern is a discrete analogue of a plane wave with wavevector (A, B)
folded onto Z/NZ.
"""

def build_grid(n: int = 9, a: int = 2, b: int = 3) -> list:
    """Return the n x n grid of (x*a + y*b) % n values, indexed [y][x]."""
    return [[(x * a + y * b) % n for x in range(n)] for y in range(n)]


def render_html(n: int = 9, a: int = 2, b: int = 3, cell_size: int = 30, canvas_id: str = "cv") -> str:
    """Build the HTML/canvas markup for the (x*a + y*b) % n grid."""
    dim = n * cell_size
    return f"""
<canvas id="{canvas_id}" width="{dim}" height="{dim}" style="border:1px solid #444;"></canvas>
<script>
    (function() {{
        const cv = document.getElementById('{canvas_id}');
        const ctx = cv.getContext('2d');
        const size = {cell_size};
        const n = {n};
        const A = {a};
        const B = {b};

        ctx.font = "14px Arial";
        for (let y = 0; y < n; y++) {{
            for (let x = 0; x < n; x++) {{
                let val = (x * A + y * B) % n;
                ctx.strokeRect(x * size, y * size, size, size);
                ctx.fillText(val, x * size + 10, y * size + 20);
            }}
        }}
    }})();
</script>
"""


def show(n: int = 9, a: int = 2, b: int = 3, cell_size: int = 30) -> None:
    """Display the grid inline in a Jupyter/IPython notebook."""
    from IPython.display import HTML, display

    display(HTML(render_html(n=n, a=a, b=b, cell_size=cell_size)))


if __name__ == "__main__":
    for row in build_grid():
        print(" ".join(str(v) for v in row))
