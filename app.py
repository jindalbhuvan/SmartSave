import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px

from src.financial_engine import calculate_financial_plan

# NEW: MySQL-based spending analyzer
from src.mysql_spending_analyzer import (
    load_mysql_transactions,
    get_customer_transactions,
    generate_spending_summary
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartSave",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.brand {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
}

.brand-subtitle {
    font-size: 13px;
    color: #6b7280;
}

.hero {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 55px 45px;
    margin: 25px 0 30px 0;
}

.hero-title {
    font-size: 46px;
    font-weight: 750;
    line-height: 1.1;
    color: #111827;
    margin-bottom: 15px;
}

.hero-text {
    font-size: 18px;
    color: #6b7280;
    max-width: 650px;
    line-height: 1.6;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    margin-top: 30px;
    margin-bottom: 20px;
}

.feature-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
    min-height: 150px;
}

.feature-title {
    font-size: 19px;
    font-weight: 650;
    color: #111827;
    margin-bottom: 10px;
}

.feature-text {
    font-size: 14px;
    color: #6b7280;
    line-height: 1.6;
}

.goal-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.goal-icon {
    font-size: 32px;
    margin-bottom: 10px;
}

.goal-title {
    font-size: 17px;
    font-weight: 650;
    color: #111827;
}

.insight-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 500;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "results" not in st.session_state:
    st.session_state.results = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    return f"₹{value:,.0f}"


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# NAVIGATION BAR
# ============================================================

nav1, nav2, nav3, nav4, nav5 = st.columns(
    [2.5, 1, 1, 1.4, 1]
)

with nav1:

    st.markdown(
        """
<div class="brand">💰 SmartSave</div>
<div class="brand-subtitle">
Personal Finance & Financial Wellness
</div>
""",
        unsafe_allow_html=True
    )

with nav2:

    if st.button("Home", use_container_width=True):
        go_to("home")

with nav3:

    if st.button("My Plan", use_container_width=True):
        go_to("results")

with nav4:

    if st.button("Spending", use_container_width=True):
        go_to("spending")

with nav5:

    if st.button("Create Plan", use_container_width=True):
        go_to("planning")


st.divider()


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        """
<div class="hero">

<div class="hero-title">
Plan smarter.<br>
Save with purpose.
</div>

<div class="hero-text">
SmartSave helps you understand your spending,
build realistic financial goals, and create a
personalized savings plan.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Create Your Financial Plan →",
            use_container_width=True
        ):
            go_to("planning")


    with col2:

        if st.button(
            "Analyze My Spending →",
            use_container_width=True
        ):
            go_to("spending")


    st.markdown(
        '<div class="section-title">'
        'Everything you need to save smarter'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
🎯 Goal Planning
</div>

<div class="feature-text">
Set financial goals and understand exactly
how much you need to save every month.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
📊 Spending Analysis
</div>

<div class="feature-text">
Understand where your money goes and
identify areas where you can save more.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
<div class="feature-card">

<div class="feature-title">
❤️ Financial Health
</div>

<div class="feature-text">
Get a financial health score based on
savings, expenses, debt and emergency
fund coverage.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">'
        'Popular financial goals'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    goals = [
        ("🛵", "Buy a Bike"),
        ("🚗", "Buy a Car"),
        ("✈️", "Travel"),
        ("🏠", "Buy a Home")
    ]


    for col, (icon, title) in zip(
        [col1, col2, col3, col4],
        goals
    ):

        with col:

            st.markdown(
                f"""
<div class="goal-card">

<div class="goal-icon">
{icon}
</div>

<div class="goal-title">
{title}
</div>

</div>
""",
                unsafe_allow_html=True
            )


# ============================================================
# FINANCIAL PLANNING PAGE
# ============================================================

elif st.session_state.page == "planning":

    st.markdown(
        '<div class="section-title">'
        'Create Your Financial Plan'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter your monthly financial information and your goal."
    )


    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    st.markdown("### Monthly Income")

    income = st.number_input(
        "Monthly Income (₹)",
        min_value=15000.0,
        max_value=1000000.0,
        value=50000.0,
        step=1000.0
    )


    # --------------------------------------------------------
    # EXPENSES
    # --------------------------------------------------------

    st.markdown("### Monthly Expenses")

    st.caption(
        "SmartSave prevents total planned expenses "
        "from exceeding 90% of monthly income."
    )


    expense_limit = income * 0.90


    col1, col2, col3 = st.columns(3)


    with col1:

        rent = st.number_input(
            "Rent",
            min_value=0.0,
            max_value=income * 0.45,
            value=min(10000.0, income * 0.20),
            step=500.0
        )

        food = st.number_input(
            "Food",
            min_value=0.0,
            max_value=income * 0.20,
            value=min(5000.0, income * 0.10),
            step=500.0
        )

        transport = st.number_input(
            "Transport",
            min_value=0.0,
            max_value=income * 0.15,
            value=min(2500.0, income * 0.05),
            step=500.0
        )


    with col2:

        utilities = st.number_input(
            "Utilities",
            min_value=0.0,
            max_value=income * 0.10,
            value=min(2000.0, income * 0.05),
            step=500.0
        )

        shopping = st.number_input(
            "Shopping",
            min_value=0.0,
            max_value=income * 0.15,
            value=min(3000.0, income * 0.06),
            step=500.0
        )

        entertainment = st.number_input(
            "Entertainment",
            min_value=0.0,
            max_value=income * 0.10,
            value=min(2000.0, income * 0.04),
            step=500.0
        )


    with col3:

        insurance = st.number_input(
            "Insurance",
            min_value=0.0,
            max_value=income * 0.15,
            value=min(1500.0, income * 0.03),
            step=500.0
        )

        subscriptions = st.number_input(
            "Subscriptions",
            min_value=0.0,
            max_value=income * 0.05,
            value=min(500.0, income * 0.01),
            step=100.0
        )

        other_expenses = st.number_input(
            "Other Expenses",
            min_value=0.0,
            max_value=income * 0.10,
            value=min(1000.0, income * 0.02),
            step=500.0
        )

        monthly_emi = st.number_input(
            "Monthly EMI",
            min_value=0.0,
            max_value=income * 0.40,
            value=0.0,
            step=500.0
        )


    total_planned_expenses = (
        rent
        + food
        + transport
        + utilities
        + shopping
        + entertainment
        + insurance
        + subscriptions
        + other_expenses
        + monthly_emi
    )


    if total_planned_expenses > expense_limit:

        st.error(
            f"Your planned expenses are "
            f"{money(total_planned_expenses)}, "
            f"but SmartSave allows a maximum of "
            f"{money(expense_limit)}."
        )

        st.warning(
            "Please reduce your expenses before "
            "creating the financial plan."
        )

        st.stop()


    # --------------------------------------------------------
    # CURRENT FINANCIAL POSITION
    # --------------------------------------------------------

    st.markdown("### Current Financial Position")


    col1, col2 = st.columns(2)


    with col1:

        current_savings = st.number_input(
            "Current Savings (₹)",
            min_value=0.0,
            max_value=10000000.0,
            value=50000.0,
            step=1000.0
        )


    with col2:

        emergency_fund = st.number_input(
            "Emergency Fund (₹)",
            min_value=0.0,
            max_value=10000000.0,
            value=30000.0,
            step=1000.0
        )


    # --------------------------------------------------------
    # FINANCIAL GOAL
    # --------------------------------------------------------

    st.markdown("### Your Financial Goal")


    col1, col2 = st.columns(2)


    with col1:

        goal_type = st.selectbox(
            "Goal Type",
            [
                "Emergency Fund",
                "Bike",
                "Car",
                "Education",
                "Travel",
                "Home",
                "Business",
                "Custom"
            ]
        )


        target_amount = st.number_input(
            "Target Amount (₹)",
            min_value=10000.0,
            max_value=100000000.0,
            value=200000.0,
            step=5000.0
        )


    with col2:

        goal_saved = st.number_input(
            "Already Saved for Goal (₹)",
            min_value=0.0,
            max_value=target_amount,
            value=0.0,
            step=1000.0
        )


        target_date = st.date_input(
            "Target Date",
            min_value=date.today(),
            max_value=date(
                date.today().year + 20,
                date.today().month,
                date.today().day
            ),
            value=date(
                date.today().year + 2,
                date.today().month,
                date.today().day
            )
        )


    if goal_saved > target_amount:

        st.error(
            "Amount already saved cannot be greater "
            "than the target amount."
        )

        st.stop()


    # --------------------------------------------------------
    # CALCULATE PLAN
    # --------------------------------------------------------

    if st.button(
        "Calculate My Plan →",
        use_container_width=True
    ):

        results = calculate_financial_plan(

            income=income,

            rent=rent,
            food=food,
            transport=transport,
            utilities=utilities,
            shopping=shopping,
            entertainment=entertainment,
            insurance=insurance,
            subscriptions=subscriptions,
            other_expenses=other_expenses,

            monthly_emi=monthly_emi,

            current_savings=current_savings,
            emergency_fund=emergency_fund,

            goal_type=goal_type,
            target_amount=target_amount,
            goal_saved=goal_saved,
            target_date=target_date
        )


        st.session_state.results = results

        go_to("results")


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.page == "results":

    results = st.session_state.results


    if results is None:

        st.markdown(
            '<div class="section-title">'
            'My Financial Plan'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "You haven't created a financial plan yet."
        )


        if st.button("Create My Plan →"):
            go_to("planning")


    else:

        st.markdown(
            '<div class="section-title">'
            'Your SmartSave Plan'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # FINANCIAL OVERVIEW
        # ----------------------------------------------------

        st.markdown("### Financial Overview")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Monthly Income",
                money(results["income"])
            )


        with col2:

            st.metric(
                "Monthly Expenses",
                money(results["total_expenses"])
            )


        with col3:

            st.metric(
                "Monthly Surplus",
                money(results["monthly_surplus"])
            )


        with col4:

            st.metric(
                "Savings Rate",
                f"{results['savings_rate']:.1f}%"
            )


        # ----------------------------------------------------
        # FINANCIAL RATIOS
        # ----------------------------------------------------

        st.markdown("### Financial Ratios")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Expense-to-Income",
                f"{results['expense_ratio']:.1f}%"
            )


        with col2:

            st.metric(
                "Debt-to-Income",
                f"{results['debt_to_income']:.1f}%"
            )


        with col3:

            st.metric(
                "Essential Expense Ratio",
                f"{results['essential_expense_ratio']:.1f}%"
            )


        with col4:

            st.metric(
                "Emergency Coverage",
                f"{results['emergency_fund_months']:.1f} months"
            )


        # ----------------------------------------------------
        # GOAL PROGRESS
        # ----------------------------------------------------

        st.markdown("### Goal Progress")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Goal",
                results["goal_type"]
            )


        with col2:

            st.metric(
                "Target Amount",
                money(results["target_amount"])
            )


        with col3:

            st.metric(
                "Remaining",
                money(results["remaining_goal"])
            )


        # ----------------------------------------------------
        # MONTHLY SAVING REQUIREMENT
        # ----------------------------------------------------

        st.markdown("### Monthly Saving Requirement")


        st.metric(
            "Required Monthly Saving",
            money(results["required_monthly_saving"])
        )


        if results["goal_achievable"]:

            st.success(
                "Your current monthly surplus is sufficient "
                "to reach this goal within the target period."
            )

        else:

            st.warning(
                "Your current monthly surplus may not be "
                "enough to reach this goal within the target period."
            )


        # ----------------------------------------------------
        # HEALTH SCORE
        # ----------------------------------------------------

        st.markdown(
            "### SmartSave Financial Health Score"
        )


        st.progress(
            results["health_score"] / 100
        )


        st.metric(
            "Health Score",
            f"{results['health_score']} / 100"
        )


        # ----------------------------------------------------
        # ASSESSMENT
        # ----------------------------------------------------

        st.markdown("### SmartSave Assessment")


        if results["health_score"] >= 80:

            st.success(
                "Your current financial structure shows "
                "strong savings capacity, manageable debt "
                "and healthy expense levels."
            )


        elif results["health_score"] >= 60:

            st.info(
                "Your financial position is reasonably "
                "balanced, but there are areas where "
                "financial resilience can be improved."
            )


        elif results["health_score"] >= 40:

            st.warning(
                "Your financial position requires attention. "
                "Consider improving savings and controlling "
                "expenses or debt."
            )


        else:

            st.error(
                "Your current financial structure indicates "
                "limited financial resilience."
            )


        # ----------------------------------------------------
        # INSIGHT
        # ----------------------------------------------------

        st.markdown(
            """
<div class="insight-card">

<h3>💡 SmartSave Insight</h3>

<p>
SmartSave evaluates your financial position using
income, expenses, savings, debt obligations,
emergency-fund coverage and goal requirements.
</p>

</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# SPENDING ANALYSIS PAGE — MYSQL
# ============================================================

elif st.session_state.page == "spending":

    st.markdown(
        '<div class="section-title">'
        'Spending Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Analyze transaction behaviour and understand "
        "where your money is being spent."
    )


    # --------------------------------------------------------
    # LOAD DATA FROM MYSQL
    # --------------------------------------------------------

    try:

        df = load_mysql_transactions()

    except Exception as e:

        st.error(
            "Unable to load transaction data from MySQL."
        )

        st.exception(e)

        st.stop()


    # --------------------------------------------------------
    # CUSTOMER SELECTION
    # --------------------------------------------------------

    customers = sorted(
        df["customer_id"].unique()
    )


    selected_customer = st.selectbox(
        "Select Customer",
        customers
    )


    customer_df = get_customer_transactions(
        df,
        selected_customer
    )


    summary = generate_spending_summary(
        customer_df
    )


    # --------------------------------------------------------
    # FINANCIAL OVERVIEW
    # --------------------------------------------------------

    st.markdown("### Financial Overview")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Income",
            money(summary["total_income"])
        )


    with col2:

        st.metric(
            "Total Expenses",
            money(summary["total_expenses"])
        )


    with col3:

        st.metric(
            "Savings",
            money(summary["savings"])
        )


    with col4:

        st.metric(
            "Savings Rate",
            f"{summary['savings_rate']:.1f}%"
        )


    # --------------------------------------------------------
    # SPENDING BEHAVIOUR
    # --------------------------------------------------------

    st.markdown("### Spending Behaviour")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Essential Spending",
            money(summary["essential_spending"])
        )


    with col2:

        st.metric(
            "Discretionary Spending",
            money(summary["discretionary_spending"])
        )


    with col3:

        top_category = (
            summary["top_spending_category"]
            or "N/A"
        )

        st.metric(
            "Top Spending Category",
            top_category
        )


    # --------------------------------------------------------
    # CATEGORY SPENDING
    # --------------------------------------------------------

    st.markdown("### Spending Breakdown")


    category_spending = (
        customer_df[
            customer_df["transaction_type"] == "Expense"
        ]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


    if not category_spending.empty:

        col1, col2 = st.columns(2)


        with col1:

            chart_df = (
                category_spending
                .reset_index()
            )

            chart_df.columns = [
                "Category",
                "Amount"
            ]


            fig_bar = px.bar(
                chart_df,
                x="Category",
                y="Amount",
                title="Spending by Category"
            )


            fig_bar.update_layout(
                xaxis_title="",
                yaxis_title="Amount (₹)",
                height=400
            )


            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )


        with col2:

            fig_pie = px.pie(
                chart_df,
                names="Category",
                values="Amount",
                title="Expense Distribution"
            )


            fig_pie.update_layout(
                height=400
            )


            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )


        # ----------------------------------------------------
        # CATEGORY DETAILS
        # ----------------------------------------------------

        st.markdown(
            "### Category-wise Spending Details"
        )


        display_df = (
            category_spending
            .reset_index()
        )


        display_df.columns = [
            "Category",
            "Amount"
        ]


        display_df["Amount"] = (
            display_df["Amount"].round(2)
        )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No expense transactions found."
        )


    # --------------------------------------------------------
    # ESSENTIAL VS DISCRETIONARY
    # --------------------------------------------------------

    st.markdown(
        "### Essential vs Discretionary Spending"
    )


    essential = summary[
        "essential_spending"
    ]

    discretionary = summary[
        "discretionary_spending"
    ]


    comparison_df = pd.DataFrame(
        {
            "Type": [
                "Essential",
                "Discretionary"
            ],

            "Amount": [
                essential,
                discretionary
            ]
        }
    )


    fig_comparison = px.bar(
        comparison_df,
        x="Type",
        y="Amount",
        title="Essential vs Discretionary Expenses",
        text="Amount"
    )


    fig_comparison.update_layout(
        xaxis_title="",
        yaxis_title="Amount (₹)",
        height=350
    )


    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )


    # --------------------------------------------------------
    # MONTHLY FINANCIAL TREND
    # --------------------------------------------------------

    st.markdown(
        "### Monthly Financial Trend"
    )


    monthly_df = customer_df.copy()


    monthly_df["month"] = (
        monthly_df["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_income = (
        monthly_df[
            monthly_df["transaction_type"] == "Income"
        ]
        .groupby("month")["amount"]
        .sum()
    )


    monthly_expenses = (
        monthly_df[
            monthly_df["transaction_type"] == "Expense"
        ]
        .groupby("month")["amount"]
        .sum()
    )


    monthly_financials = pd.DataFrame(
        {
            "Income": monthly_income,
            "Expenses": monthly_expenses
        }
    ).fillna(0)


    monthly_financials["Savings"] = (
        monthly_financials["Income"]
        - monthly_financials["Expenses"]
    )


    monthly_financials = (
        monthly_financials
        .reset_index()
    )


    trend_df = monthly_financials.melt(
        id_vars="month",
        value_vars=[
            "Income",
            "Expenses",
            "Savings"
        ],
        var_name="Metric",
        value_name="Amount"
    )


    fig_trend = px.line(
        trend_df,
        x="month",
        y="Amount",
        color="Metric",
        markers=True,
        title="Income, Expenses and Savings Trend"
    )


    fig_trend.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (₹)",
        height=450
    )


    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )


    # --------------------------------------------------------
    # SMARTSAVE SPENDING INSIGHTS
    # --------------------------------------------------------

    st.markdown(
        "### SmartSave Spending Insights"
    )


    top_category = (
        summary["top_spending_category"]
    )


    if top_category:

        top_category_amount = (
            category_spending[top_category]
        )


        st.info(
            f"Your highest spending category is "
            f"**{top_category}**, with spending of "
            f"**₹{top_category_amount:,.0f}**."
        )


    discretionary_ratio = (

        discretionary
        / summary["total_income"] * 100

        if summary["total_income"] > 0

        else 0
    )


    if discretionary_ratio > 25:

        st.warning(
            f"Discretionary spending represents "
            f"approximately {discretionary_ratio:.1f}% "
            f"of your income. Reducing discretionary "
            f"expenses could improve your savings capacity."
        )


    elif discretionary_ratio > 15:

        st.info(
            f"Discretionary spending is approximately "
            f"{discretionary_ratio:.1f}% of income."
        )


    else:

        st.success(
            f"Discretionary spending is relatively "
            f"controlled at "
            f"{discretionary_ratio:.1f}% of income."
        )