(function () {
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
    ];

    function formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            maximumFractionDigits: 2,
        }).format(value || 0);
    }

    function setupCanvas(canvas) {
        if (!canvas) {
            return null;
        }
        const context = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        const width = canvas.clientWidth || 320;
        const height = canvas.clientHeight || 160;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        context.scale(dpr, dpr);
        context.clearRect(0, 0, width, height);
        context.fillStyle = '#0f172a';
        context.fillRect(0, 0, width, height);
        context.translate(0.5, 0.5);
        return { context, width, height };
    }

    function renderDonutChart(canvasId, labels, values, colors) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !values.length) {
            return;
        }
        const setup = setupCanvas(canvas);
        if (!setup) {
            return;
        }
        const { context: ctx, width, height } = setup;
        const total = values.reduce((acc, value) => acc + value, 0);
        if (total <= 0) {
            return;
        }
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.4;
        let startAngle = -Math.PI / 2;

        values.forEach((value, index) => {
            const sliceAngle = (value / total) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.fillStyle = colors[index] || palette[index % palette.length];
            ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
            ctx.closePath();
            ctx.fill();
            startAngle += sliceAngle;
        });

        ctx.fillStyle = '#0f172a';
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.55, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#CBD5F5';
        ctx.font = 'bold 16px system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(formatCurrency(total), centerX, centerY + 6);
    }

    function renderHorizontalBarChart(canvasId, labels, values) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !values.length) {
            return;
        }
        const setup = setupCanvas(canvas);
        if (!setup) {
            return;
        }
        const { context: ctx, width, height } = setup;
        const maxValue = Math.max(...values, 1);
        const barHeight = Math.min(36, height / (values.length + 0.5));
        const gap = barHeight * 0.4;
        const leftPadding = 140;
        const chartWidth = width - leftPadding - 20;

        ctx.font = '12px system-ui, sans-serif';
        ctx.fillStyle = '#CBD5F5';
        ctx.textBaseline = 'middle';

        values.forEach((value, index) => {
            const y = barHeight / 2 + index * (barHeight + gap) + 20;
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(leftPadding, y - barHeight / 2, chartWidth, barHeight);

            const barWidth = (value / maxValue) * chartWidth;
            ctx.fillStyle = '#38BDF8';
            ctx.fillRect(leftPadding, y - barHeight / 2, barWidth, barHeight);

            ctx.fillStyle = '#CBD5F5';
            ctx.textAlign = 'right';
            ctx.fillText(labels[index], leftPadding - 10, y);

            ctx.textAlign = 'left';
            ctx.fillText(formatCurrency(value), leftPadding + barWidth + 10, y);
        });
    }

    function renderLineChart(canvasId, labels, primarySeries, secondarySeries, targetSeries) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !(primarySeries.length || secondarySeries.length)) {
            return;
        }
        const setup = setupCanvas(canvas);
        if (!setup) {
            return;
        }
        const { context: ctx, width, height } = setup;
        const padding = { left: 60, right: 20, top: 20, bottom: 40 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;

        const values = [...primarySeries, ...secondarySeries, ...(targetSeries || [])];
        const maxValue = Math.max(...values, 1);

        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        const gridLines = 4;
        for (let i = 0; i <= gridLines; i += 1) {
            const y = padding.top + (chartHeight / gridLines) * i;
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            const gridValue = maxValue - (maxValue / gridLines) * i;
            ctx.fillStyle = '#64748b';
            ctx.font = '11px system-ui, sans-serif';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            ctx.fillText(formatCurrency(gridValue), padding.left - 8, y);
        }

        function drawSeries(series, color, fill) {
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            series.forEach((value, index) => {
                const x = padding.left + (chartWidth / Math.max(labels.length - 1, 1)) * index;
                const y = padding.top + chartHeight - (chartHeight * (value / maxValue));
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.stroke();
            if (fill) {
                ctx.lineTo(padding.left + chartWidth, padding.top + chartHeight);
                ctx.lineTo(padding.left, padding.top + chartHeight);
                ctx.closePath();
                ctx.fillStyle = fill;
                ctx.fill();
            }
        }

        if (primarySeries.length) {
            drawSeries(primarySeries, '#22C55E', 'rgba(34, 197, 94, 0.12)');
        }
        if (secondarySeries.length) {
            drawSeries(secondarySeries, '#F87171', 'rgba(248, 113, 113, 0.12)');
        }
        if (targetSeries && targetSeries.length) {
            ctx.setLineDash([5, 4]);
            drawSeries(targetSeries, '#94A3B8');
            ctx.setLineDash([]);
        }

        ctx.fillStyle = '#CBD5F5';
        ctx.font = '11px system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        labels.forEach((label, index) => {
            const x = padding.left + (chartWidth / Math.max(labels.length - 1, 1)) * index;
            ctx.fillText(label, x, height - padding.bottom + 12);
        });
    }

    function renderGroupedBars(canvasId, labels, series) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !labels.length) {
            return;
        }
        const setup = setupCanvas(canvas);
        if (!setup) {
            return;
        }
        const { context: ctx, width, height } = setup;
        const padding = { left: 60, right: 20, top: 20, bottom: 40 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;
        const groupWidth = chartWidth / labels.length;
        const barWidth = groupWidth / (series.length + 1);

        const values = series.flatMap((item) => item.values);
        const maxValue = Math.max(...values, 1);

        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        const gridLines = 4;
        for (let i = 0; i <= gridLines; i += 1) {
            const y = padding.top + (chartHeight / gridLines) * i;
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            const gridValue = maxValue - (maxValue / gridLines) * i;
            ctx.fillStyle = '#64748b';
            ctx.font = '11px system-ui, sans-serif';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            ctx.fillText(formatCurrency(gridValue), padding.left - 8, y);
        }

        labels.forEach((label, index) => {
            const baseX = padding.left + index * groupWidth;
            series.forEach((serie, serieIndex) => {
                const value = serie.values[index] || 0;
                const barHeight = (value / maxValue) * chartHeight;
                const x = baseX + barWidth * (serieIndex + 0.2);
                const y = padding.top + chartHeight - barHeight;
                ctx.fillStyle = serie.color || palette[(serieIndex + index) % palette.length];
                ctx.fillRect(x, y, barWidth * 0.8, barHeight);
            });
            ctx.fillStyle = '#CBD5F5';
            ctx.font = '11px system-ui, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            const labelX = baseX + groupWidth / 2;
            ctx.fillText(label, labelX, height - padding.bottom + 12);
        });
    }

    function renderComboBarLine(canvasId, labels, income, expense, balance) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !labels.length) {
            return;
        }
        const setup = setupCanvas(canvas);
        if (!setup) {
            return;
        }
        const { context: ctx, width, height } = setup;
        const padding = { left: 70, right: 30, top: 20, bottom: 40 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;
        const barWidth = chartWidth / labels.length / 3;

        const values = [...income, ...expense, ...balance];
        const maxValue = Math.max(...values, 1);

        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        const gridLines = 4;
        for (let i = 0; i <= gridLines; i += 1) {
            const y = padding.top + (chartHeight / gridLines) * i;
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            const gridValue = maxValue - (maxValue / gridLines) * i;
            ctx.fillStyle = '#64748b';
            ctx.font = '11px system-ui, sans-serif';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            ctx.fillText(formatCurrency(gridValue), padding.left - 10, y);
        }

        labels.forEach((label, index) => {
            const groupX = padding.left + index * (chartWidth / labels.length);
            const incomeHeight = (income[index] / maxValue) * chartHeight;
            const expenseHeight = (expense[index] / maxValue) * chartHeight;

            ctx.fillStyle = '#22C55E';
            ctx.fillRect(groupX, padding.top + chartHeight - incomeHeight, barWidth, incomeHeight);

            ctx.fillStyle = '#EF4444';
            ctx.fillRect(groupX + barWidth + 4, padding.top + chartHeight - expenseHeight, barWidth, expenseHeight);

            ctx.fillStyle = '#CBD5F5';
            ctx.font = '11px system-ui, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            ctx.fillText(label, groupX + barWidth, height - padding.bottom + 12);
        });

        ctx.strokeStyle = '#38BDF8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        labels.forEach((label, index) => {
            const x = padding.left + index * (chartWidth / labels.length) + barWidth;
            const y = padding.top + chartHeight - (chartHeight * (balance[index] / maxValue));
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();
    }

    window.FinanpyCharts = {
        renderDonutChart,
        renderHorizontalBarChart,
        renderLineChart,
        renderGroupedBars,
        renderComboBarLine,
    };
}());
