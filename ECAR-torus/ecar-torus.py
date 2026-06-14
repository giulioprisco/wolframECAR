import numpy as np
import plotly.graph_objects as go

# ====================== CORE RULE 37R ======================
def rule_37r_next(prev: int, curr: int, N: int) -> int:
    next_curr = 0
    for i in range(N):
        l = (curr >> ((i - 1) % N)) & 1
        c = (curr >> i) & 1
        r = (curr >> ((i + 1) % N)) & 1
        neigh_idx = (l << 2) | (c << 1) | r
        rule_bit = (37 >> neigh_idx) & 1
        prev_bit = (prev >> i) & 1
        next_bit = rule_bit ^ prev_bit
        if next_bit:
            next_curr |= (1 << i)
    return next_curr


def get_canonical(seed: int, N: int) -> int:
    min_seed = seed
    current = seed
    mask = (1 << N) - 1
    for _ in range(N - 1):
        current = ((current << 1) & mask) | (current >> (N - 1))
        if current < min_seed:
            min_seed = current
    return min_seed


def evolve_to_grid(seed: int, N: int, period: int) -> np.ndarray:
    grid = np.zeros((period + 1, N), dtype=int)
    prev = 0
    curr = seed
    for j in range(N):
        grid[0, j] = (curr >> j) & 1
    for t in range(1, period + 1):
        nxt = rule_37r_next(prev, curr, N)
        for j in range(N):
            grid[t, j] = (nxt >> j) & 1
        prev, curr = curr, nxt
    return grid


# ====================== PLOTLY TORUS (thick doughnut) ======================
def plot_torus_plotly(seed: int, N: int, period: int, pattern_idx: int = 1, total_patterns: int = 1):
    grid = evolve_to_grid(seed, N, period)
    
    R = 6.0
    r = 3.5
    
    dtheta = 2 * np.pi / N
    dphi   = 2 * np.pi / (period + 1)
    
    vertices = []
    faces = []
    face_colors = []
    
    for t in range(period + 1):
        for i in range(N):
            phi0 = t * dphi
            phi1 = (t + 1) * dphi
            theta0 = i * dtheta
            theta1 = (i + 1) * dtheta
            
            def torus_point(phi, theta):
                x = (R + r * np.cos(theta)) * np.cos(phi)
                y = (R + r * np.cos(theta)) * np.sin(phi)
                z = r * np.sin(theta)
                return [x, y, z]
            
            v0 = torus_point(phi0, theta0)
            v1 = torus_point(phi0, theta1)
            v2 = torus_point(phi1, theta1)
            v3 = torus_point(phi1, theta0)
            
            idx = len(vertices)
            vertices.extend([v0, v1, v2, v3])
            
            faces.append([idx, idx+1, idx+2])
            faces.append([idx, idx+2, idx+3])
            
            color = '#000000' if grid[t, i] else '#ffffff'
            face_colors.extend([color, color])
    
    x, y, z = zip(*vertices)
    ijk = np.array(faces).T
    
    fig = go.Figure(data=[
        go.Mesh3d(
            x=x, y=y, z=z,
            i=ijk[0], j=ijk[1], k=ijk[2],
            facecolor=face_colors,
            opacity=1.0,
            lighting=dict(ambient=0.7, diffuse=0.8, specular=0.3),
            flatshading=True
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"Rule 37R — True 3D Torus (thick doughnut)<br>"
                 f"Period = {period} | N = {N} | Seed = 0b{bin(seed)[2:].zfill(N)} "
                 f"(Pattern {pattern_idx}/{total_patterns})",
            x=0.5, y=0.96, xanchor='center', yanchor='top',
            font=dict(size=18, color="black")
        ),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=2.2, y=-2.0, z=1.8)),
            aspectmode='manual',
            aspectratio=dict(x=3.0, y=1.0, z=1.0)
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        width=1800,
        height=700,
        paper_bgcolor='#e5e5e5',
        plot_bgcolor='#e5e5e5'
    )
    
    fig.show()


# ====================== OPTIMIZED SEARCH WITH CLEAN PERCENTAGE UPDATES ======================
def find_max_period_37r_distinct(N: int):
    total_starts = 1 << N
    max_period = 0
    max_seeds = []

    print(f"Searching N={N} ({total_starts:,} seeds)...")

    percent_step = max(1, total_starts // 100)   # update every 1%

    for c in range(total_starts):
        prev = 0
        curr = c
        seen = {}
        step = 0
        state = (prev, curr)

        while state not in seen:
            seen[state] = step
            nxt = rule_37r_next(prev, curr, N)
            prev, curr = curr, nxt
            state = (prev, curr)
            step += 1
            if step > 200_000:
                break

        if state in seen:
            period = step - seen[state]
            if period > max_period:
                max_period = period
                max_seeds = [c]
            elif period == max_period:
                max_seeds.append(c)

        # Print percentage only when it changes (1%, 2%, ...)
        if (c + 1) % percent_step == 0 or c + 1 == total_starts:
            percent = (c + 1) * 100 // total_starts
            print(f"  {percent}% done", end="\r")

    print("\nSearch finished.")

    # Deduplicate by rotation
    canonical_set = {get_canonical(s, N) for s in max_seeds}
    unique_reps = sorted(list(canonical_set))

    print(f"\n=== RESULTS for N={N} ===")
    print(f"Longest repeat period: {max_period}")
    print(f"Total seeds achieving this period: {len(max_seeds)}")
    print(f"Distinct patterns up to rotation: {len(unique_reps)}")
    for rep in unique_reps:
        bin_str = f'{rep:0{N}b}'
        print(f"  {bin_str}  →  {' '.join(bin_str[::-1])}")

    if unique_reps:
        print(f"\nOpening {len(unique_reps)} thick-torus plots...")
        for idx, rep in enumerate(unique_reps):
            plot_torus_plotly(rep, N, max_period, idx+1, len(unique_reps))

    return max_period, unique_reps


if __name__ == "__main__":
    N = int(input("Enter N (e.g. 9, 12, 16): "))
    find_max_period_37r_distinct(N)
