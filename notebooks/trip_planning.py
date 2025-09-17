# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pydeck",
#     "pandas",
#     "ipython",
# ]
# ///

import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import pydeck as pdk

    return mo, pd, pdk


@app.cell
def _(mo):
    mo.md(
        r"""
    Maximum Coastal Route - Seaford to Eastbourne

     Day 1: Seaford → Cuckmere Haven/Seven Sisters Country Park

     Distance: 8-10 miles (with exploration)
     - Walk to Cuckmere Haven (4 miles)
     - Explore coastguard cottages, beach, meanders
     - Continue to Seven Sisters Country Park visitor center
     - Stay: Saltdean Farm B&B or wild camp at Foxhole Campsite (both near coast)
     - If needed, return bus to Seaford for more accommodation options

     Day 2: Seven Sisters → Birling Gap

     Distance: 9-10 miles
     - Complete full Seven Sisters clifftop walk
     - Lunch at Birling Gap beach café
     - Stay: Birling Gap Hotel (literally on the clifftop!)
     - Alternative: Tiger Inn in East Dean (1 mile inland but closest village)

     Day 3: Birling Gap → Eastbourne

     Distance: 8-10 miles (with coastal detours)
     - Via Beachy Head lighthouse viewpoint
     - Optional: Add Belle Tout lighthouse loop
     - Descend via coastal path (not inland route) to Eastbourne seafront
     - Walk full promenade before station

     Even MORE Coastal - Add Camping

     Wild camping isn't technically allowed BUT:
     - YHA Camping: Seven Sisters Country Park has basic camping
     - Beachy Head Campsite: Near East Dean, close to cliffs
     - Foxhole Campsite: Near Cuckmere Haven

     Pro Coastal Tips

     - Birling Gap Hotel is THE must-stay for maximum coastal experience
     - Pack lunch/snacks - limited facilities between towns
     - Low tide timing at Birling Gap = beach walking opportunity
     - Book Birling Gap Hotel well ahead (small, very popular)

     This route keeps you within sight/sound of the sea for 90% of the walk!
    """
    )
    return


@app.cell
def _(pd):
    # Expanded route starting from London
    route_points = [
        {
            "name": "London (Start)",
            "lat": 51.49134394031131,
            "lon": -0.10514580621524008,
            "day": "Travel Day",
            "distance": "0 miles",
            "description": "Journey start - travel to Seaford",
            "accommodation": "Travel to Seaford by train",
        },
        {
            "name": "Seaford",
            "lat": 50.7719,
            "lon": 0.1019,
            "day": "Day 1 Start",
            "distance": "Train journey from London",
            "description": "Starting point of the coastal walk",
            "accommodation": "Various options in town",
        },
        {
            "name": "Cuckmere Haven",
            "lat": 50.7614,
            "lon": 0.1636,
            "day": "Day 1",
            "distance": "4 miles from Seaford",
            "description": "Explore coastguard cottages, beach, and river meanders",
            "accommodation": "Foxhole Campsite nearby",
        },
        {
            "name": "Seven Sisters Country Park",
            "lat": 50.7580,
            "lon": 0.1800,
            "day": "Day 1 End",
            "distance": "8-10 miles total",
            "description": "Visitor center and start of famous Seven Sisters cliffs",
            "accommodation": "YHA Camping, Saltdean Farm B&B",
        },
        {
            "name": "Birling Gap",
            "lat": 50.7420,
            "lon": 0.2058,
            "day": "Day 2 End",
            "distance": "9-10 miles from Seven Sisters",
            "description": "Beach café, clifftop hotel, low tide beach walking opportunity",
            "accommodation": "Birling Gap Hotel (clifftop!), Tiger Inn in East Dean",
        },
        {
            "name": "Belle Tout Lighthouse",
            "lat": 50.7380,
            "lon": 0.2300,
            "day": "Day 3 (Optional)",
            "distance": "Loop from Beachy Head",
            "description": "Optional lighthouse loop with dramatic cliff views",
            "accommodation": "Day visit only",
        },
        {
            "name": "Beachy Head",
            "lat": 50.7364,
            "lon": 0.2434,
            "day": "Day 3",
            "distance": "En route to Eastbourne",
            "description": "Lighthouse viewpoint, optional Belle Tout lighthouse loop",
            "accommodation": "Beachy Head Campsite near East Dean",
        },
        {
            "name": "Eastbourne",
            "lat": 50.7684,
            "lon": 0.2903,
            "day": "Finish",
            "distance": "8-10 miles from Birling Gap",
            "description": "Walk full promenade to station, coastal route complete",
            "accommodation": "Town center options, then return to London",
        },
    ]

    # Update the route DataFrame
    route_df = pd.DataFrame(route_points)

    # Create directed path coordinates (showing flow of journey)
    path_coordinates = [[point["lon"], point["lat"]] for point in route_points]
    return path_coordinates, route_df


@app.cell
def _(path_coordinates, pdk, route_df):
    # Create directed path layer with arrow-like styling
    _directed_path_layer = pdk.Layer(
        "PathLayer",
        data=[{"path": path_coordinates}],
        get_path="path",
        get_width=20,
        get_color="[0, 150, 200, 200]",
        pickable=True,
    )

    # Different colors for different stages of journey
    def get_point_color(day):
        if "Travel" in day or "London" in day:
            return [100, 100, 100, 200]  # Gray for travel
        elif "Start" in day:
            return [0, 200, 0, 200]  # Green for start
        elif "Finish" in day:
            return [200, 0, 0, 200]  # Red for finish
        else:
            return [255, 165, 0, 200]  # Orange for walking days

    route_df["color"] = route_df["day"].apply(get_point_color)

    _directed_scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=route_df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=400,
        pickable=True,
    )

    # Create the directed route map
    _directed_coastal_map = pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=51.0,  # Centered to show both London and coast
            longitude=0.1,
            zoom=8,
            pitch=30,
            bearing=0,
        ),
        layers=[_directed_path_layer, _directed_scatter_layer],
        tooltip={
            "html": "<b>{name}</b><br/>Stage: {day}<br/>Distance: {distance}<br/>{description}",
            "style": {"backgroundColor": "rgba(0, 0, 0, 0.8)", "color": "white"},
        },
    )

    _directed_coastal_map
    return


if __name__ == "__main__":
    app.run()
