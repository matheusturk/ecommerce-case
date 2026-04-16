import reflex as rx
import duckdb
import os
from typing import TypedDict
from datetime import date, timedelta
from collections import defaultdict


# ── TypedDicts ────────────────────────────────────────────────────────────────

class CFOKPIData(TypedDict):
    total_revenue: str
    total_orders: str
    avg_ticket: str
    total_refunded: str
    refund_rate: str

class COOKPIData(TypedDict):
    total_orders: str
    total_delivered: str
    total_failed: str
    total_in_progress: str
    delivered_rate: str
    failure_rate: str
    avg_days_to_approval: str
    avg_days_to_post: str
    avg_days_to_customer: str
    avg_total_delivery_time: str

class CSKPIData(TypedDict):
    avg_review_score: str
    total_reviews: str
    avg_score_on_time: str
    avg_score_late: str

class MarketplaceKPIData(TypedDict):
    total_sellers: str
    total_revenue: str
    avg_ticket: str
    avg_freight: str
    top_category: str

class RevenueData(TypedDict):
    order_date: str
    gross_revenue: float

class PaymentData(TypedDict):
    order_date: str
    credit_card: float
    boleto: float
    voucher: float
    debit_card: float

class OrdersVolumeData(TypedDict):
    purchase_date: str
    total_orders: int
    delivered_orders: int
    failed_orders: int

class DeliveryBreakdownData(TypedDict):
    purchase_date: str
    days_to_approval: float
    days_to_post: float
    days_to_customer: float

class ReviewsTrendData(TypedDict):
    purchase_date: str
    avg_score_on_time: float
    avg_score_late: float

class ReviewsDistributionData(TypedDict):
    purchase_date: str
    score_1: float
    score_2: float
    score_3: float
    score_4: float
    score_5: float

class CategoryData(TypedDict):
    product_category: str
    total_revenue: float
    total_orders: int

class SellerData(TypedDict):
    seller_id: str
    total_revenue: float
    total_orders: int


# ── Helpers ───────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "volis_analytics",
    "dev.duckdb",
)

def _fmt_brl(v):
    if v is None: return "—"
    return f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def _fmt_int(v):
    if v is None: return "—"
    return f"{int(v):,}".replace(",",".")

def _fmt_pct(v):
    if v is None: return "—"
    return f"{v*100:.1f}".replace(".",",")

def _fmt_days(v):
    if v is None: return "—"
    return f"{v:.1f}".replace(".",",")

def _fmt_score(v):
    if v is None: return "—"
    return f"{v:.2f}".replace(".",",")

def _get_date_bounds():
    try:
        conn = duckdb.connect(DB_PATH, read_only=True)
        row = conn.execute("""
            SELECT
                CAST(MIN("CAST(order_approved_at AS DATE)") AS VARCHAR),
                CAST(MAX("CAST(order_approved_at AS DATE)") AS VARCHAR)
            FROM mart_financials
        """).fetchone()
        conn.close()
        if row and row[0] and row[1]:
            return row[0], row[1]
    except Exception as e:
        print(f"[DashboardState] Erro ao buscar datas: {e}")
    return "2016-09-04", "2018-08-31"

_REAL_START, _REAL_END = _get_date_bounds()


# ── State ─────────────────────────────────────────────────────────────────────

class DashboardState(rx.State):
    loading: bool = True

    dataset_start: str = _REAL_START
    dataset_end:   str = _REAL_END
    date_start:    str = _REAL_START
    date_end:      str = _REAL_END
    active_preset: str = "all"
    current_page:  str = "cfo"
    time_granularity: str = "day"  # "day" | "month" | "year"

    # CFO
    cfo_kpis: CFOKPIData = {
        "total_revenue":"—","total_orders":"—","avg_ticket":"—",
        "total_refunded":"—","refund_rate":"—",
    }
    revenue_over_time:    list[RevenueData] = []
    payment_distribution: list[PaymentData] = []

    # COO
    coo_kpis: COOKPIData = {
        "total_orders":"—","total_delivered":"—","total_failed":"—",
        "total_in_progress":"—","delivered_rate":"—","failure_rate":"—",
        "avg_days_to_approval":"—","avg_days_to_post":"—",
        "avg_days_to_customer":"—","avg_total_delivery_time":"—",
    }
    orders_volume:      list[OrdersVolumeData]      = []
    delivery_breakdown: list[DeliveryBreakdownData] = []

    # CS
    cs_kpis: CSKPIData = {
        "avg_review_score":"—","total_reviews":"—",
        "avg_score_on_time":"—","avg_score_late":"—",
    }
    reviews_trend:        list[ReviewsTrendData]        = []
    reviews_distribution: list[ReviewsDistributionData] = []

    # Marketplace
    marketplace_kpis: MarketplaceKPIData = {
        "total_sellers":"—","total_revenue":"—",
        "avg_ticket":"—","avg_freight":"—","top_category":"—",
    }
    top_categories: list[CategoryData] = []
    top_sellers:    list[SellerData]   = []

    # ── Helpers de agregação ──────────────────────────────────────────────────

    def _date_key(self, d: str) -> str:
        if self.time_granularity == "month":
            return d[:7]
        elif self.time_granularity == "year":
            return d[:4]
        return d

    def _aggregate_sum(self, rows: list, date_key: str, value_keys: list) -> list:
        grouped: dict = defaultdict(lambda: {k: 0.0 for k in value_keys})
        for row in rows:
            k = self._date_key(row.get(date_key, "") or "")
            for vk in value_keys:
                grouped[k][vk] += row.get(vk, 0.0) or 0.0
        return [{date_key: k, **v} for k, v in sorted(grouped.items())]

    # ── Vars computadas ───────────────────────────────────────────────────────

    @rx.var
    def revenue_over_time_agg(self) -> list[RevenueData]:
        return self._aggregate_sum(self.revenue_over_time, "order_date", ["gross_revenue"])

    @rx.var
    def payment_distribution_agg(self) -> list[PaymentData]:
        return self._aggregate_sum(
            self.payment_distribution, "order_date",
            ["credit_card", "boleto", "voucher", "debit_card"],
        )

    @rx.var
    def orders_volume_agg(self) -> list[OrdersVolumeData]:
        return self._aggregate_sum(
            self.orders_volume, "purchase_date",
            ["total_orders", "delivered_orders", "failed_orders"],
        )

    @rx.var
    def delivery_breakdown_agg(self) -> list[DeliveryBreakdownData]:
        grouped: dict = defaultdict(lambda: {
            "sum_approval": 0.0, "sum_post": 0.0, "sum_customer": 0.0, "count": 0
        })
        for row in self.delivery_breakdown:
            k = self._date_key(row.get("purchase_date", "") or "")
            grouped[k]["sum_approval"]  += row.get("days_to_approval", 0.0) or 0.0
            grouped[k]["sum_post"]      += row.get("days_to_post", 0.0) or 0.0
            grouped[k]["sum_customer"]  += row.get("days_to_customer", 0.0) or 0.0
            grouped[k]["count"]         += 1
        result = []
        for k, v in sorted(grouped.items()):
            c = v["count"] or 1
            result.append({
                "purchase_date":    k,
                "days_to_approval": round(v["sum_approval"] / c, 1),
                "days_to_post":     round(v["sum_post"] / c, 1),
                "days_to_customer": round(v["sum_customer"] / c, 1),
            })
        return result

    @rx.var
    def reviews_trend_agg(self) -> list[ReviewsTrendData]:
        grouped: dict = defaultdict(lambda: {
            "sum_on": 0.0, "cnt_on": 0, "sum_late": 0.0, "cnt_late": 0
        })
        for row in self.reviews_trend:
            k = self._date_key(row.get("purchase_date", "") or "")
            if row.get("avg_score_on_time") is not None:
                grouped[k]["sum_on"]  += row["avg_score_on_time"]
                grouped[k]["cnt_on"]  += 1
            if row.get("avg_score_late") is not None:
                grouped[k]["sum_late"] += row["avg_score_late"]
                grouped[k]["cnt_late"] += 1
        result = []
        for k, v in sorted(grouped.items()):
            result.append({
                "purchase_date":     k,
                "avg_score_on_time": round(v["sum_on"]  / v["cnt_on"],  2) if v["cnt_on"]  else None,
                "avg_score_late":    round(v["sum_late"] / v["cnt_late"],2) if v["cnt_late"] else None,
            })
        return result

    @rx.var
    def reviews_distribution_agg(self) -> list[ReviewsDistributionData]:
        return self._aggregate_sum(
            self.reviews_distribution, "purchase_date",
            ["score_1", "score_2", "score_3", "score_4", "score_5"],
        )

    # ── Eventos de filtro ─────────────────────────────────────────────────────

    def _fetch_for_current_page(self):
        if self.current_page == "cfo":
            return DashboardState.fetch_cfo_data
        elif self.current_page == "coo":
            return DashboardState.fetch_coo_data
        elif self.current_page == "cs":
            return DashboardState.fetch_cs_data
        else:
            return DashboardState.fetch_marketplace_data

    @rx.event
    def set_granularity(self, granularity: str):
        self.time_granularity = granularity

    @rx.event
    def set_current_page(self, page: str):
        self.current_page = page

    @rx.event
    def set_preset(self, preset: str):
        end = date.fromisoformat(self.dataset_end)
        self.active_preset = preset
        if preset == "1m":
            self.date_start = (end - timedelta(days=30)).isoformat()
            self.date_end   = self.dataset_end
        elif preset == "3m":
            self.date_start = (end - timedelta(days=90)).isoformat()
            self.date_end   = self.dataset_end
        elif preset == "6m":
            self.date_start = (end - timedelta(days=180)).isoformat()
            self.date_end   = self.dataset_end
        else:
            self.date_start = self.dataset_start
            self.date_end   = self.dataset_end
        yield self._fetch_for_current_page()

    @rx.event
    def set_date_start(self, value: str):
        self.date_start    = value
        self.active_preset = "custom"
        yield self._fetch_for_current_page()

    @rx.event
    def set_date_end(self, value: str):
        self.date_end      = value
        self.active_preset = "custom"
        yield self._fetch_for_current_page()

    @rx.event
    def fetch_dashboard_data(self):
        pass

    # ── Fetch por página ──────────────────────────────────────────────────────

    @rx.event
    def fetch_cfo_data(self):
        self.loading = True
        yield
        try:
            conn = duckdb.connect(DB_PATH, read_only=True)
            ds, de = self.date_start, self.date_end

            row = conn.execute(f"""
                SELECT SUM(gross_revenue), SUM(total_orders),
                    SUM(gross_revenue)/NULLIF(SUM(total_orders),0),
                    SUM(refunded_revenue),
                    SUM(refunded_revenue)/NULLIF(SUM(gross_revenue),0)
                FROM mart_financials
                WHERE "CAST(order_approved_at AS DATE)" BETWEEN '{ds}' AND '{de}'
            """).fetchone()
            if row:
                self.cfo_kpis = {
                    "total_revenue": _fmt_brl(row[0]), "total_orders": _fmt_int(row[1]),
                    "avg_ticket": _fmt_brl(row[2]), "total_refunded": _fmt_brl(row[3]),
                    "refund_rate": _fmt_pct(row[4]),
                }

            rows = conn.execute(f"""
                SELECT CAST("CAST(order_approved_at AS DATE)" AS VARCHAR), gross_revenue
                FROM mart_financials
                WHERE "CAST(order_approved_at AS DATE)" BETWEEN '{ds}' AND '{de}'
                ORDER BY 1
            """).fetchall()
            self.revenue_over_time = [
                {"order_date": r[0], "gross_revenue": round(float(r[1]), 2)} for r in rows
            ]

            rows = conn.execute(f"""
                SELECT CAST(order_date AS VARCHAR), payment_type, total_payment_value
                FROM mart_payment_distribution
                WHERE order_date BETWEEN '{ds}' AND '{de}'
                ORDER BY 1
            """).fetchall()
            pm: dict = {}
            for od, pt, v in rows:
                if od not in pm:
                    pm[od] = {"order_date":od,"credit_card":0.0,"boleto":0.0,"voucher":0.0,"debit_card":0.0}
                k = pt.lower().replace(" ","_")
                if k in pm[od]:
                    pm[od][k] += round(float(v), 2)
            self.payment_distribution = list(pm.values())
            conn.close()
        except Exception as e:
            print(f"[CFO] Erro: {e}")
        finally:
            self.loading = False

    @rx.event
    def fetch_coo_data(self):
        self.loading = True
        yield
        try:
            conn = duckdb.connect(DB_PATH, read_only=True)
            ds, de = self.date_start, self.date_end

            row = conn.execute(f"""
                SELECT SUM(total_orders), SUM(delivered_orders), SUM(failed_orders),
                    SUM(in_progress_orders),
                    SUM(delivered_orders)*1.0/NULLIF(SUM(total_orders),0),
                    SUM(failed_orders)*1.0/NULLIF(SUM(total_orders),0),
                    AVG(days_to_approval), AVG(days_to_post),
                    AVG(days_to_customer), AVG(total_delivery_time)
                FROM mart_orders
                WHERE purchase_date BETWEEN '{ds}' AND '{de}'
            """).fetchone()
            if row:
                self.coo_kpis = {
                    "total_orders": _fmt_int(row[0]), "total_delivered": _fmt_int(row[1]),
                    "total_failed": _fmt_int(row[2]), "total_in_progress": _fmt_int(row[3]),
                    "delivered_rate": _fmt_pct(row[4]), "failure_rate": _fmt_pct(row[5]),
                    "avg_days_to_approval": _fmt_days(row[6]), "avg_days_to_post": _fmt_days(row[7]),
                    "avg_days_to_customer": _fmt_days(row[8]), "avg_total_delivery_time": _fmt_days(row[9]),
                }

            rows = conn.execute(f"""
                SELECT CAST(purchase_date AS VARCHAR), total_orders, delivered_orders, failed_orders
                FROM mart_orders WHERE purchase_date BETWEEN '{ds}' AND '{de}'
                ORDER BY purchase_date
            """).fetchall()
            self.orders_volume = [
                {"purchase_date":r[0],"total_orders":int(r[1]),
                 "delivered_orders":int(r[2]),"failed_orders":int(r[3])} for r in rows
            ]

            rows = conn.execute(f"""
                SELECT CAST(purchase_date AS VARCHAR),
                    COALESCE(days_to_approval,0), COALESCE(days_to_post,0), COALESCE(days_to_customer,0)
                FROM mart_orders
                WHERE purchase_date BETWEEN '{ds}' AND '{de}' AND total_delivery_time IS NOT NULL
                ORDER BY purchase_date
            """).fetchall()
            self.delivery_breakdown = [
                {"purchase_date":r[0],"days_to_approval":round(float(r[1]),1),
                 "days_to_post":round(float(r[2]),1),"days_to_customer":round(float(r[3]),1)} for r in rows
            ]
            conn.close()
        except Exception as e:
            print(f"[COO] Erro: {e}")
        finally:
            self.loading = False

    @rx.event
    def fetch_cs_data(self):
        self.loading = True
        yield
        try:
            conn = duckdb.connect(DB_PATH, read_only=True)
            ds, de = self.date_start, self.date_end

            row = conn.execute(f"""
                SELECT AVG(avg_review_score), SUM(total_reviews),
                    AVG(CASE WHEN delivery_status='on_time' THEN avg_review_score END),
                    AVG(CASE WHEN delivery_status='late'    THEN avg_review_score END)
                FROM mart_reviews_vs_delivery
                WHERE purchase_date BETWEEN '{ds}' AND '{de}'
            """).fetchone()
            if row:
                self.cs_kpis = {
                    "avg_review_score": _fmt_score(row[0]), "total_reviews": _fmt_int(row[1]),
                    "avg_score_on_time": _fmt_score(row[2]), "avg_score_late": _fmt_score(row[3]),
                }

            rows = conn.execute(f"""
                SELECT CAST(purchase_date AS VARCHAR),
                    AVG(CASE WHEN delivery_status='on_time' THEN avg_review_score END),
                    AVG(CASE WHEN delivery_status='late'    THEN avg_review_score END)
                FROM mart_reviews_vs_delivery
                WHERE purchase_date BETWEEN '{ds}' AND '{de}'
                GROUP BY purchase_date ORDER BY purchase_date
            """).fetchall()
            self.reviews_trend = [
                {"purchase_date":r[0],
                 "avg_score_on_time": round(float(r[1]),2) if r[1] else None,
                 "avg_score_late":    round(float(r[2]),2) if r[2] else None} for r in rows
            ]

            rows = conn.execute(f"""
                SELECT CAST(purchase_date AS VARCHAR), review_score, review_count
                FROM mart_reviews_distribution
                WHERE purchase_date BETWEEN '{ds}' AND '{de}'
                ORDER BY purchase_date, review_score
            """).fetchall()
            dm: dict = {}
            for pd_, sc, cnt in rows:
                if pd_ not in dm:
                    dm[pd_] = {"purchase_date":pd_,"score_1":0.0,"score_2":0.0,
                               "score_3":0.0,"score_4":0.0,"score_5":0.0}
                k = f"score_{int(sc)}"
                if k in dm[pd_]:
                    dm[pd_][k] += float(cnt)
            self.reviews_distribution = list(dm.values())
            conn.close()
        except Exception as e:
            print(f"[CS] Erro: {e}")
        finally:
            self.loading = False

    @rx.event
    def fetch_marketplace_data(self):
        self.loading = True
        yield
        try:
            conn = duckdb.connect(DB_PATH, read_only=True)
            ds, de = self.date_start, self.date_end

            row = conn.execute(f"""
                SELECT COUNT(DISTINCT i.seller_id), SUM(i.price),
                    SUM(i.price)/NULLIF(COUNT(DISTINCT i.order_id),0),
                    AVG(i.freight_value)
                FROM int_order_items i
                JOIN int_orders o ON i.order_id = o.order_id
                WHERE DATE(o.order_purchase_timestamp) BETWEEN '{ds}' AND '{de}'
            """).fetchone()
            if row:
                self.marketplace_kpis = {
                    "total_sellers": _fmt_int(row[0]), "total_revenue": _fmt_brl(row[1]),
                    "avg_ticket": _fmt_brl(row[2]), "avg_freight": _fmt_brl(row[3]),
                    "top_category": "—",
                }

            top_cat = conn.execute(f"""
                SELECT COALESCE(i.product_category_name,'unknown')
                FROM int_order_items i
                JOIN int_orders o ON i.order_id = o.order_id
                WHERE DATE(o.order_purchase_timestamp) BETWEEN '{ds}' AND '{de}'
                GROUP BY 1 ORDER BY SUM(i.price) DESC LIMIT 1
            """).fetchone()
            if top_cat:
                self.marketplace_kpis = {**self.marketplace_kpis, "top_category": top_cat[0]}

            rows = conn.execute(f"""
                SELECT COALESCE(i.product_category_name,'unknown'),
                    SUM(i.price), COUNT(DISTINCT i.order_id)
                FROM int_order_items i
                JOIN int_orders o ON i.order_id = o.order_id
                WHERE DATE(o.order_purchase_timestamp) BETWEEN '{ds}' AND '{de}'
                GROUP BY 1 ORDER BY 2 DESC LIMIT 15
            """).fetchall()
            self.top_categories = [
                {"product_category":r[0],"total_revenue":round(float(r[1]),2),"total_orders":int(r[2])}
                for r in rows
            ]

            rows = conn.execute(f"""
                SELECT i.seller_id, SUM(i.price), COUNT(DISTINCT i.order_id)
                FROM int_order_items i
                JOIN int_orders o ON i.order_id = o.order_id
                WHERE DATE(o.order_purchase_timestamp) BETWEEN '{ds}' AND '{de}'
                GROUP BY i.seller_id ORDER BY 2 DESC LIMIT 15
            """).fetchall()
            self.top_sellers = [
                {"seller_id": r[0][:8]+"...", "total_revenue":round(float(r[1]),2),
                 "total_orders":int(r[2])}
                for r in rows
            ]
            conn.close()
        except Exception as e:
            print(f"[Marketplace] Erro: {e}")
        finally:
            self.loading = False