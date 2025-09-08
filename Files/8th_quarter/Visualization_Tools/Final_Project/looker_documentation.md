# xpert-IA Strategic Dashboard Documentation

## Introduction

This document provides a detailed overview of the 5-page **xpert-IA Strategic Dashboard**. Built with data from `tech_salaries`, this report is designed to be a dynamic tool for executive decision-making. Its purpose is to transform raw market data into actionable intelligence across four key business pillars: Compensation, Talent Strategy, Competitive Positioning, and Strategic Growth.

Each page is structured to answer a fundamental business question, enabling data-driven strategies for hiring, budgeting, and market positioning. This documentation will walk through the purpose and key analyses of each page.

---

## Page 1: Salary Market Intelligence & Evolution

### Purpose

This page answers the foundational question: **"How much should we pay to be competitive?"**. It provides a comprehensive view of salary benchmarks and how they have evolved over time, allowing for the creation of fair, competitive, and data-backed compensation packages.

### Key Analyses & Insights

* **Salary Benchmarking by Role & Experience**
    * **What it shows:** This analysis uses box plots to display the full salary range—from minimum to maximum, including the median (50th percentile) and interquartile ranges (25th-75th percentile)—for our core technical roles. Each role is further segmented by experience level (Entry, Mid, Senior, Executive).
    * **Strategic Value:** It allows us to move beyond simple averages and understand the complete compensation landscape. This is critical for defining precise salary bands for new hires and ensuring internal pay scales are aligned with the external market.

* **Salary Evolution by Role (Trend Analysis)**
    * > **ANALYSIS:** Identify roles with accelerating salary growth (steeper lines). This signals rising demand and potential talent scarcity. Is the salary for "AI Engineer" growing faster than for "Data Scientist"?
    * **Explanation:** By tracking the median salary of key job titles over time, we can identify which specializations are becoming more valuable (and expensive) in the market. A steep upward trend in a role's salary line is a leading indicator of a "hot" market, suggesting we may need to adjust our budgets upward to attract and retain talent in that area.

* **Salary Evolution by Experience Level (Gap Analysis)**
    * > **ANALYSIS:** Compare the slopes. A steeper line for senior/executive levels indicates a widening salary gap. This informs promotion budgets and senior hiring strategy. Are we paying a higher premium for senior talent year-over-year?
    * **Explanation:** This chart compares the salary growth rates across different seniority levels. If the line for Senior (`SE`) or Executive (`EX`) talent is rising faster than for Mid-level (`MI`) or Entry-level (`EN`) talent, it means the premium for experience is increasing. This insight is crucial for structuring promotion-based raises and justifying the budget required to hire top-tier senior leadership.

---

## Page 2: Talent & Work Model Strategy

### Purpose

This page addresses the operational question: **"How should we structure our team in the new work paradigm?"**. It analyzes the relationship between work models (remote, hybrid, on-site), talent location, and hiring patterns to help design a flexible and effective global talent strategy.

### Key Analyses & Insights

* **Work Model Preference by Experience**
    * > **ANALYSIS:** Are senior and executive roles more likely to be remote? This data informs our remote work policy and helps attract talent at different experience levels.
    * **Explanation:** This analysis breaks down the preference for remote, hybrid, and on-site work by experience level. If we observe that top-level talent overwhelmingly prefers remote work, it provides a strong case for implementing a remote-first or flexible policy to avoid limiting our talent pool.

* **Hiring Patterns by Role**
    * > **ANALYSIS:** Is Full-Time (FT) the dominant model for all our core roles, or are there opportunities to leverage contractors (CT) or freelancers (FL) for specific skills? This helps optimize hiring flexibility and costs.
    * **Explanation:** This chart shows the distribution of employment types (Full-Time, Contract, Freelance) for our core job titles. If certain specialized roles show a high prevalence of contractors in the market, it suggests we could leverage a flexible workforce model for specific projects, optimizing costs and accessing specialized skills without the overhead of a full-time hire.

* **Global Talent Supply vs. Demand**
    * > **ANALYSIS:** Identify gaps between supply and demand. Are there countries with a high concentration of talent (green map) but low company presence (blue map)? These are prime locations for remote hiring and represent a key strategic advantage.
    * **Explanation:** By visualizing talent residence (`Supply`) and company location (`Demand`) on two separate world maps, we can spot geographic arbitrage opportunities. A country with a large talent pool but few hiring companies is a market where we can likely find high-quality talent with less competition, giving us a significant strategic advantage in building a global team.

---

## Page 3: Competitive Landscape & Positioning

### Purpose

This page focuses on answering the competitive question: **"Where do we stand against the competition?"**. It analyzes how competitors of different sizes operate, which roles they prioritize, and where the market is heading, allowing us to position **xpert-IA** intelligently.

### Key Analyses & Insights

* **Salary Premiums by Company Size**
    * > **ANALYSIS:** Identify the salary gap between Large ('L') and Small/Medium ('S'/'M') companies for our key roles. This is our direct competition. Can we compete on salary, or should we focus on other benefits?
    * **Explanation:** This chart directly compares the median salaries offered by small, medium, and large companies for the same roles. Understanding the "premium" that large enterprises pay helps us realistically assess our position. If we cannot match their salaries, this data provides the impetus to strengthen our competitive offer in other areas, such as equity, culture, or impactful work.

* **Current Top-Paying Roles**
    * > **ANALYSIS:** These are the market's most expensive roles today. This signals high demand and specialization. How does our current salary structure compare for these critical roles?
    * **Explanation:** This analysis provides a simple, ranked list of the most expensive job titles in the current market. It acts as a real-time snapshot of where the highest value is being placed. This is a critical gut-check to ensure our own compensation for these high-demand roles is not falling dangerously behind the market.

* **Identifying "Talent Bubbles"**
    * > **ANALYSIS:** Look for the steepest lines. A role with a rapidly increasing salary indicates a potential "talent bubble" or scarcity. This helps us anticipate future salary pressures and hire strategically.
    * **Explanation:** Similar to the analysis on Page 1, but viewed through a competitive lens. Identifying a role whose salary is skyrocketing allows us to anticipate a "bidding war." This insight can prompt a strategy to either hire for that skill set *before* the market peaks or to develop that talent internally to avoid the high cost of external hiring.

---

## Pages 4 & 5: Hidden Opportunities & Strategic Insights

### Purpose

This final section is designed to answer the most crucial strategic question: **"What is our competition not seeing?"**. It moves beyond standard analysis to uncover outliers, anomalies, and undervalued opportunities that can provide a unique competitive edge.

### Key Analyses & Insights

* **Atypical Patterns: High-Value Talent in Startups**
    * > **ANALYSIS:** Pay close attention to the outliers (dots) above the main box for 'S' (Small) companies. These represent highly-paid senior talent in startups. It proves that small companies CAN attract top-tier talent if they are willing to be competitive on compensation for critical roles.
    * **Explanation:** By isolating senior and executive roles, this chart looks for instances where small companies are paying salaries that are statistical outliers—often on par with or exceeding large-company offers. These data points are powerful proof points that startups can and do win top talent. They serve as a benchmark for what it takes to hire a "game-changer" and justify a top-of-market offer for a critical hire.

* **Identifying Undervalued Global Talent Pools**
    * > **ANALYSIS:** Look for countries with dots that are significantly below the main cluster, especially for the 'SE' and 'EX' colors. Countries like Poland (PL), Spain (ES), or Brazil (BR) might have senior talent at a fraction of the cost of the US or UK. These are prime targets for building a high-impact, cost-effective global team.
    * **Explanation:** This is the "treasure map" for global hiring. The scatter plot visualizes countries based on the median salary for senior talent. The countries that appear low on the vertical axis represent markets where the cost of high-quality, experienced talent is significantly lower than in primary markets like the US. These are our "blue ocean" opportunities for building skilled, cost-effective teams and extending our operational runway.