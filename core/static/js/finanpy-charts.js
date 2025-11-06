(function () {
    if (typeof window === 'undefined') {
        return;
    }

    const palette = [
        '#6366F1',
        '#3B82F6',
        '#8B5CF6',
        '#22C55E',
        '#10B981',
        '#F59E0B',
        '#EC4899',
        '#EF4444',
        '#38BDF8',
        '#F97316',
        '#FCD34D',
        '#14B8A6',
    ];

    function formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            maximumFractionDigits: 2,
        }).format(value || 0);
    }

    function getFallbackColor(index) {
        return palette[index % palette.length];
    }

    function resolveValue(context) {
        const parsed = context.parsed;
        if (parsed === null || typeof parsed === 'undefined') {
            return 0;
        }
        if (typeof parsed === 'object') {
            if (typeof parsed.y === 'number') {
                return parsed.y;
            }
            if (typeof parsed.x === 'number') {
                return parsed.x;
            }
        }
        return parsed;
    }

    function computeAxisBounds(seriesCollection) {
        const values = [];
        (seriesCollection || []).forEach((series) => {
            if (!Array.isArray(series)) {
                return;
            }
            series.forEach((value) => {
                if (typeof value === 'number' && Number.isFinite(value)) {
                    values.push(value);
                }
            });
        });
        if (!values.length) {
            return {};
        }
        const max = Math.max(...values);
        const min = Math.min(...values);
        const paddingBase = Math.max(Math.abs(max), Math.abs(min), 1);
        const padding = paddingBase * 0.08;
        const bounds = {};
        if (min >= 0) {
            bounds.beginAtZero = true;
            bounds.suggestedMax = max + padding;
        } else if (max <= 0) {
            bounds.beginAtZero = false;
            bounds.suggestedMin = min - padding;
        } else {
            bounds.beginAtZero = false;
            bounds.suggestedMax = max + padding;
            bounds.suggestedMin = min - padding;
        }
        return bounds;
    }

    function buildCurrencyTooltip() {
        return {
            intersect: false,
            mode: 'index',
            backgroundColor: 'rgba(15, 23, 42, 0.92)',
            borderColor: 'rgba(148, 163, 184, 0.35)',
            borderWidth: 1,
            padding: 12,
            displayColors: true,
            callbacks: {
                label(context) {
                    const prefix = context.dataset && context.dataset.label ? `${context.dataset.label}: ` : '';
                    return `${prefix}${formatCurrency(resolveValue(context))}`;
                },
            },
        };
    }

    function buildCurrencyTicks() {
        return {
            color: '#94A3B8',
            font: { size: 12 },
            callback(value) {
                return formatCurrency(value);
            },
        };
    }

    const layoutPadding = { top: 16, right: 20, bottom: 16, left: 20 };
    const chartInstances = new Map();

    function destroyChart(canvasId) {
        const chart = chartInstances.get(canvasId);
        if (chart) {
            chart.destroy();
            chartInstances.delete(canvasId);
        }
    }

    function registerChart(canvasId, config) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            return null;
        }
        destroyChart(canvasId);
        const chart = new window.Chart(canvas, config);
        chartInstances.set(canvasId, chart);
        return chart;
    }

    if (typeof window.Chart === 'undefined') {
        console.warn('[FinanpyCharts] Chart.js não foi carregado; os gráficos não serão renderizados.');
        window.FinanpyCharts = {
            renderDonutChart: () => {},
            renderHorizontalBarChart: () => {},
            renderLineChart: () => {},
            renderGroupedBars: () => {},
            renderComboBarLine: () => {},
            destroy: destroyChart,
            destroyAll() {
                chartInstances.forEach((_, key) => destroyChart(key));
            },
        };
        return;
    }

    const { Chart } = window;

    Chart.defaults.color = '#E2E8F0';
    Chart.defaults.borderColor = 'rgba(148, 163, 184, 0.35)';
    Chart.defaults.font.family =
        'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.font.weight = 500;
    Chart.defaults.animation.duration = 550;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.boxWidth = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.titleFont.weight = 600;
    Chart.defaults.plugins.tooltip.bodyFont.weight = 500;
    Chart.defaults.elements.point.radius = 4;
    Chart.defaults.elements.point.hoverRadius = 6;
    Chart.defaults.elements.point.backgroundColor = '#F8FAFC';
    Chart.defaults.elements.point.borderWidth = 0;
    Chart.defaults.elements.line.tension = 0.35;

    function createCenterLabelPlugin(text) {
        return {
            id: 'finanpyCenterLabel',
            afterDraw(chart) {
                if (!text) {
                    return;
                }
                const meta = chart.getDatasetMeta(0);
                if (!meta || !meta.data || !meta.data.length) {
                    return;
                }
                const { ctx } = chart;
                const { x, y } = meta.data[0];
                ctx.save();
                ctx.fillStyle = '#F8FAFC';
                ctx.font = '600 16px system-ui, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(text, x, y);
                ctx.restore();
            },
        };
    }

    function renderDonutChart(canvasId, labels, values, colors) {
        if (!values || !values.length) {
            destroyChart(canvasId);
            return;
        }
        const total = values.reduce((acc, item) => acc + (item || 0), 0);
        if (!total) {
            destroyChart(canvasId);
            return;
        }
        const datasetColors = Array.isArray(colors) && colors.length
            ? colors
            : values.map((_, index) => getFallbackColor(index));
        registerChart(canvasId, {
            type: 'doughnut',
            data: {
                labels,
                datasets: [
                    {
                        data: values,
                        backgroundColor: datasetColors,
                        borderColor: '#0F172A',
                        borderWidth: 2,
                        hoverOffset: 10,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: { padding: layoutPadding },
                cutout: '68%',
                plugins: {
                    tooltip: {
                        ...buildCurrencyTooltip(),
                        callbacks: {
                            label(context) {
                                const label = context.label ? `${context.label}: ` : '';
                                return `${label}${formatCurrency(resolveValue(context))}`;
                            },
                        },
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#CBD5F5',
                        },
                    },
                },
            },
            plugins: [createCenterLabelPlugin(formatCurrency(total))],
        });
    }

    function renderHorizontalBarChart(canvasId, labels, values) {
        if (!values || !values.length) {
            destroyChart(canvasId);
            return;
        }
        const bounds = computeAxisBounds([values]);
        registerChart(canvasId, {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Saldo',
                        data: values,
                        backgroundColor: '#38BDF8',
                        borderRadius: 9,
                        borderSkipped: false,
                        maxBarThickness: 32,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                layout: { padding: layoutPadding },
                interaction: { mode: 'nearest', intersect: false },
                scales: {
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.12)' },
                        ticks: buildCurrencyTicks(),
                        ...bounds,
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#CBD5F5' },
                    },
                },
                plugins: {
                    legend: { display: false },
                    tooltip: buildCurrencyTooltip(),
                },
            },
        });
    }

    function renderLineChart(canvasId, labels, incomeSeries, expenseSeries, targetSeries) {
        const hasPrimary = Array.isArray(incomeSeries) && incomeSeries.length;
        const hasSecondary = Array.isArray(expenseSeries) && expenseSeries.length;
        if (
            !hasPrimary &&
            !hasSecondary &&
            !(Array.isArray(targetSeries) && targetSeries.length)
        ) {
            destroyChart(canvasId);
            return;
        }
        const datasets = [];
        if (hasPrimary) {
            datasets.push({
                label: 'Receitas',
                data: incomeSeries,
                borderColor: '#22C55E',
                backgroundColor: 'rgba(34, 197, 94, 0.18)',
                fill: 'origin',
                pointBackgroundColor: '#22C55E',
            });
        }
        if (hasSecondary) {
            datasets.push({
                label: 'Despesas',
                data: expenseSeries,
                borderColor: '#EF4444',
                backgroundColor: 'rgba(239, 68, 68, 0.14)',
                fill: false,
                pointBackgroundColor: '#EF4444',
            });
        }
        if (Array.isArray(targetSeries) && targetSeries.length) {
            datasets.push({
                label: 'Meta de gastos (80%)',
                data: targetSeries,
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.12)',
                fill: false,
                borderDash: [6, 6],
                pointRadius: 0,
                pointHoverRadius: 0,
            });
        }
        const bounds = computeAxisBounds([incomeSeries, expenseSeries, targetSeries]);
        registerChart(canvasId, {
            type: 'line',
            data: {
                labels,
                datasets,
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: { padding: layoutPadding },
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.12)' },
                        ticks: { color: '#CBD5F5' },
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.15)' },
                        ticks: buildCurrencyTicks(),
                        ...bounds,
                    },
                },
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: buildCurrencyTooltip(),
                },
            },
        });
    }

    function renderGroupedBars(canvasId, labels, datasetConfigs) {
        if (!Array.isArray(datasetConfigs) || !datasetConfigs.length) {
            destroyChart(canvasId);
            return;
        }
        const datasets = datasetConfigs.map((config, index) => ({
            label:
                config && config.label
                    ? config.label
                    : index === 0
                    ? 'Receitas'
                    : index === 1
                    ? 'Despesas'
                    : `Série ${index + 1}`,
            data:
                config && Array.isArray(config.values)
                    ? config.values
                    : [],
            backgroundColor:
                config && config.color ? config.color : getFallbackColor(index),
            borderRadius: 7,
            borderSkipped: false,
            maxBarThickness: 28,
        }));
        const bounds = computeAxisBounds(datasets.map((dataset) => dataset.data));
        registerChart(canvasId, {
            type: 'bar',
            data: {
                labels,
                datasets,
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: { padding: layoutPadding },
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.12)' },
                        ticks: { color: '#CBD5F5' },
                        stacked: false,
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.15)' },
                        ticks: buildCurrencyTicks(),
                        ...bounds,
                    },
                },
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: buildCurrencyTooltip(),
                },
            },
        });
    }

    function renderComboBarLine(canvasId, labels, incomeSeries, expenseSeries, balanceSeries) {
        const hasIncome = Array.isArray(incomeSeries) && incomeSeries.length;
        const hasExpense = Array.isArray(expenseSeries) && expenseSeries.length;
        const hasBalance = Array.isArray(balanceSeries) && balanceSeries.length;
        if (!hasIncome && !hasExpense && !hasBalance) {
            destroyChart(canvasId);
            return;
        }
        const datasets = [];
        if (hasIncome) {
            datasets.push({
                type: 'bar',
                label: 'Receitas',
                data: incomeSeries,
                backgroundColor: '#22C55E',
                borderRadius: 7,
                borderSkipped: false,
                maxBarThickness: 26,
                order: 2,
            });
        }
        if (hasExpense) {
            datasets.push({
                type: 'bar',
                label: 'Despesas',
                data: expenseSeries,
                backgroundColor: '#EF4444',
                borderRadius: 7,
                borderSkipped: false,
                maxBarThickness: 26,
                order: 2,
            });
        }
        if (hasBalance) {
            datasets.push({
                type: 'line',
                label: 'Saldo',
                data: balanceSeries,
                borderColor: '#38BDF8',
                backgroundColor: 'rgba(56, 189, 248, 0.20)',
                borderWidth: 2,
                fill: false,
                tension: 0.35,
                pointBackgroundColor: '#38BDF8',
                order: 1,
            });
        }
        const bounds = computeAxisBounds([
            incomeSeries,
            expenseSeries,
            balanceSeries,
        ]);
        registerChart(canvasId, {
            type: 'bar',
            data: {
                labels,
                datasets,
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: { padding: layoutPadding },
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.12)' },
                        ticks: { color: '#CBD5F5' },
                    },
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.15)' },
                        ticks: buildCurrencyTicks(),
                        ...bounds,
                    },
                },
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: buildCurrencyTooltip(),
                },
            },
        });
    }

    window.FinanpyCharts = {
        renderDonutChart,
        renderHorizontalBarChart,
        renderLineChart,
        renderGroupedBars,
        renderComboBarLine,
        destroy: destroyChart,
        destroyAll() {
            chartInstances.forEach((_, key) => destroyChart(key));
        },
    };
}());
