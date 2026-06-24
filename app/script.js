document.addEventListener('DOMContentLoaded', () => {
    // Chart.js Default Config for Dark Theme
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
    Chart.defaults.font.family = "'Inter', sans-serif";

    // Formatters
    const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val);
    const formatNumber = (val) => new Intl.NumberFormat('en-US').format(val);

    fetch('insights.json')
        .then(response => response.json())
        .then(data => {
            renderKPIs(data.kpis);
            renderInsights(data.kpis);
            renderCharts(data);
            renderTargetTable(data.target_achievement);
            renderProductsTable(data.top_products);
            renderRecommendations(data.recommendations);
        })
        .catch(error => {
            console.error('Error loading insights data:', error);
            document.getElementById('kpi-container').innerHTML = '<p style="color: red;">Error loading data. Make sure insights.json exists.</p>';
        });

    function renderKPIs(kpis) {
        const container = document.getElementById('kpi-container');
        const kpiData = [
            { title: 'Total Revenue', value: formatCurrency(kpis.total_revenue), class: 'positive' },
            { title: 'Total Profit', value: formatCurrency(kpis.total_profit), class: 'positive' },
            { title: 'Total Orders', value: formatNumber(kpis.total_orders), class: '' },
            { title: 'Avg Order Value', value: formatCurrency(kpis.avg_order_value), class: '' },
            { title: 'Profit Margin', value: kpis.profit_margin.toFixed(2) + '%', class: kpis.profit_margin > 10 ? 'positive' : '' },
            { title: 'Total Shipping', value: formatCurrency(kpis.total_shipping_cost), class: 'negative' }
        ];

        kpiData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'glass-card kpi-card';
            card.innerHTML = `
                <span class="kpi-title">${item.title}</span>
                <span class="kpi-value ${item.class}">${item.value}</span>
            `;
            container.appendChild(card);
        });
    }

    function renderInsights(kpis) {
        const container = document.getElementById('insights-container');
        // Since we don't have these specific strings in the generated kpis from python natively without string formatting,
        // wait, I used the python script to generate some. Let's check the python script output structure.
        // Actually, python script has kpis with these exact strings? 
        // No, the python script had 'Best Region', 'Best Category', etc. printed but NOT in JSON `kpis` dict.
        // Wait! The Python script generate_insights.py only put numeric KPIs in `kpis` dict.
        // I need to extract best region from `sales_by_region` dynamically in JS.

        let bestRegion = Object.keys(window.dashboardData?.sales_by_region || {}).length ? '' : '...';
        // We'll compute it here.
    }

    // Overriding renderInsights to compute dynamically
    function renderInsightsCompute(data) {
        const container = document.getElementById('insights-container');
        
        // Find Best Region
        let bestRegion = Object.keys(data.sales_by_region).reduce((a, b) => data.sales_by_region[a] > data.sales_by_region[b] ? a : b);
        let bestCategory = Object.keys(data.profit_by_category).reduce((a, b) => data.profit_by_category[a] > data.profit_by_category[b] ? a : b);

        const insightData = [
            { label: 'Top Revenue Region', value: bestRegion },
            { label: 'Most Profitable Category', value: bestCategory },
            { label: 'Highest Selling Product', value: data.top_products[0]?.Product_Name || 'N/A' },
            { label: 'Most Used Payment', value: Object.keys(data.payment_method_distribution).reduce((a, b) => data.payment_method_distribution[a] > data.payment_method_distribution[b] ? a : b) }
        ];

        insightData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'glass-card insight-card';
            card.innerHTML = `
                <div class="insight-label">${item.label}</div>
                <div class="insight-data">${item.value}</div>
            `;
            container.appendChild(card);
        });
    }

    function renderCharts(data) {
        window.dashboardData = data; // for global access
        renderInsightsCompute(data); // call here when data is fully available

        // 1. Monthly Sales Trend (Line)
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        new Chart(document.getElementById('monthlySalesChart'), {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Total Sales ($)',
                    data: data.monthly_sales,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // 2. Sales by Region (Bar)
        new Chart(document.getElementById('salesRegionChart'), {
            type: 'bar',
            data: {
                labels: Object.keys(data.sales_by_region),
                datasets: [{
                    label: 'Sales ($)',
                    data: Object.values(data.sales_by_region),
                    backgroundColor: '#8b5cf6',
                    borderRadius: 4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // 3. Profit by Category (Bar)
        new Chart(document.getElementById('profitCategoryChart'), {
            type: 'bar',
            data: {
                labels: Object.keys(data.profit_by_category),
                datasets: [{
                    label: 'Profit ($)',
                    data: Object.values(data.profit_by_category),
                    backgroundColor: '#10b981',
                    borderRadius: 4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y' }
        });

        // 4. Payment Method (Donut)
        new Chart(document.getElementById('paymentMethodChart'), {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.payment_method_distribution),
                datasets: [{
                    data: Object.values(data.payment_method_distribution),
                    backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981', '#ef4444', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, cutout: '70%' }
        });

        // 5. Target Achievement (Grouped Bar)
        const regions = data.target_achievement.map(d => d.Region);
        const actuals = data.target_achievement.map(d => d.Total_Sales);
        const targets = data.target_achievement.map(d => d.Sales_Target);

        new Chart(document.getElementById('targetAchievementChart'), {
            type: 'bar',
            data: {
                labels: regions,
                datasets: [
                    {
                        label: 'Actual Sales',
                        data: actuals,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    },
                    {
                        label: 'Target',
                        data: targets,
                        backgroundColor: 'rgba(255, 255, 255, 0.2)',
                        borderRadius: 4
                    }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    function renderTargetTable(targets) {
        const tbody = document.querySelector('#targetTable tbody');
        targets.forEach(row => {
            const tr = document.createElement('tr');
            const statusClass = row.Status === 'Target Met' ? 'status-met' : 'status-missed';
            tr.innerHTML = `
                <td>${row.Region}</td>
                <td>${formatCurrency(row.Sales_Target)}</td>
                <td>${formatCurrency(row.Total_Sales)}</td>
                <td>${row.Achievement_Percent.toFixed(1)}%</td>
                <td><span class="status-badge ${statusClass}">${row.Status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderProductsTable(products) {
        const tbody = document.querySelector('#productsTable tbody');
        products.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.Product_Name}</td>
                <td>${row.Product_Category}</td>
                <td>${formatCurrency(row.Total_Sales)}</td>
                <td style="color: ${row.Profit > 0 ? '#10b981' : '#ef4444'}">${formatCurrency(row.Profit)}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderRecommendations(recs) {
        const container = document.getElementById('recommendations-container');
        recs.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'glass-card rec-card';
            card.innerHTML = `
                <div class="rec-icon">💡</div>
                <div class="rec-text">${rec}</div>
            `;
            container.appendChild(card);
        });
    }
});
