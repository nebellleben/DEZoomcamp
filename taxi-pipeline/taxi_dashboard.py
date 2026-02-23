import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def setup():
    import marimo as mo
    import dlt
    import ibis
    import altair as alt

    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data",
    )
    dataset = pipeline.dataset()
    ibis_conn = dataset.ibis()
    dataset_name = pipeline.dataset_name

    rides = ibis_conn.table("rides", database=dataset_name)

    mo.md("# NYC Taxi Trip Dashboard (June 2009)")
    return alt, ibis, ibis_conn, mo, rides


@app.cell
def payment_type_chart(alt, ibis, mo, rides):
    payment_counts = (
        rides.group_by("payment_type")
        .aggregate(trip_count=rides.payment_type.count())
        .order_by(ibis.desc("trip_count"))
    )
    df_payments = payment_counts.execute()

    payment_chart = (
        alt.Chart(df_payments)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta("trip_count:Q", stack=True),
            color=alt.Color("payment_type:N", title="Payment Type"),
            tooltip=["payment_type", "trip_count"],
        )
        .properties(title="Distribution of Payment Types", width=400, height=400)
    )

    mo.vstack([mo.md("## Payment Type Distribution"), payment_chart])
    return


@app.cell
def tips_by_date_chart(alt, ibis, mo, rides):
    tips_by_date = (
        rides.mutate(date=rides.trip_pickup_date_time.date())
        .group_by("date")
        .aggregate(total_tips=rides.tip_amt.sum())
        .order_by("date")
    )
    df_tips = tips_by_date.execute()

    tips_chart = (
        alt.Chart(df_tips)
        .mark_bar()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("total_tips:Q", title="Total Tips ($)"),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("total_tips:Q", title="Total Tips", format="$.2f"),
            ],
        )
        .properties(title="Daily Tip Revenue (June 2009)", width=700, height=400)
    )

    mo.vstack([mo.md("## Tips by Date"), tips_chart])
    return


if __name__ == "__main__":
    app.run()
