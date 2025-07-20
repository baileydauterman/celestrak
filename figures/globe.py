import plotly.graph_objects as go
from faker import Faker

fake = Faker()

lat = fake.latitude()
lon = fake.longitude()

print(f"{lat}, {lon}")

#making the plot
fig = go.Figure(
    go.Scattergeo(
        lat=[lat],
        lon=[lon]
    )
)

fig.update_traces(
    marker_size=20,
    line=dict(color='Red')
)

fig.update_geos(projection_type="orthographic")
fig.update_layout(
    width= 800,
    height=800,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig.show()