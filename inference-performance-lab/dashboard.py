from pathlib import Path
import json, pandas as pd, plotly.express as px, streamlit as st

st.set_page_config(page_title="Inference Performance Lab", layout="wide")
st.title("Inference Performance Lab")
files = sorted(Path("results").glob("*.jsonl"))
if not files:
    st.info("No results yet. Run the demo benchmark first."); st.stop()
selected = st.selectbox("Run", files, format_func=lambda p: p.name)
rows = [json.loads(x) for x in selected.read_text().splitlines() if x]
df = pd.DataFrame(rows); ok = df[df.success]
c1,c2,c3,c4 = st.columns(4)
c1.metric("Success rate", f"{df.success.mean():.1%}")
c2.metric("Median TTFT", f"{ok.ttft_ms.median():.1f} ms")
c3.metric("p95 latency", f"{ok.end_to_end_ms.quantile(.95):.1f} ms")
c4.metric("Mean quality", f"{ok.quality_score.mean():.2f}")
st.plotly_chart(px.scatter(ok, x="end_to_end_ms", y="quality_score", size="output_tokens_per_second",
                           color="target", hover_data=["model","quantization","concurrency"],
                           title="Quality vs latency (bubble size = output tokens/s)"), use_container_width=True)
summary = ok.groupby(["target","model","quantization","concurrency"]).agg(
    quality=("quality_score","mean"), p50_latency_ms=("end_to_end_ms","median"),
    p95_latency_ms=("end_to_end_ms",lambda x:x.quantile(.95)), throughput=("output_tokens_per_second","mean"),
    cost=("estimated_cost_usd","mean")).reset_index()
st.subheader("Configuration comparison"); st.dataframe(summary, use_container_width=True)
eligible = summary[summary.quality >= st.slider("Minimum acceptable quality",0.0,1.0,.8,.05)]
if len(eligible):
    best = eligible.sort_values(["cost","p95_latency_ms"], ascending=True).iloc[0]
    st.success(f"Lowest-cost eligible configuration: {best['target']} / {best['model']}. Selection is constrained by quality, then ranked by cost and tail latency.")

