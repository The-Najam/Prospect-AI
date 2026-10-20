// filepath: d:\Python\Python Programs\Prospect-Ai\frontend\app.js

const API_BASE_URL = "http://127.0.0.1:8000";
const POLL_INTERVAL = 20000;
const MAX_ATTEMPTS = 100;

const form = document.getElementById("prospect-form");
const submitButton = document.getElementById("submit-button");
const reportSection = document.getElementById("report-section");
const finalReport = document.getElementById("final-report");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Generating report...";
    reportSection.hidden = true;
    finalReport.replaceChildren();

    const formData = new FormData(form);

    const payload = {
        url: formData.get("url"),
        user_service: formData.get("user_service"),
        low_risk_offer: formData.get("low_risk_offer"),
        proof: formData.get("proof") || null,
        channel: formData.get("channel")
    };

    try {
        const response = await fetch(`${API_BASE_URL}/get_input`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const details = await response.json();
            throw new Error(JSON.stringify(details.detail, null, 2));
        }

        const data = await response.json();

        if (!data.run_id) {
            throw new Error("The backend did not return a run_id.");
        }

        await pollForReport(data.run_id);
    } catch (error) {
        renderMessage(error.message);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Generate Report";
    }
});

async function pollForReport(runId) {
    for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
        const response = await fetch(
            `${API_BASE_URL}/get_report/${encodeURIComponent(runId)}`
        );

        if (response.ok) {
            const data = await response.json();

            if (data.report) {
                renderReport(data.report);
                return;
            }
        } else if (response.status !== 404) {
            throw new Error(`Report request failed with status ${response.status}`);
        }

        await delay(POLL_INTERVAL);
    }

    throw new Error("The report was not generated within the expected time.");
}

function renderReport(report) {
    const normalizedReport =
        typeof report === "object" && report !== null
            ? report
            : { "Final Report": report };

    finalReport.replaceChildren();

    Object.entries(normalizedReport).forEach(([title, content]) => {
        const section = document.createElement("article");
        section.className = "report-card";

        const heading = document.createElement("h3");
        heading.textContent = formatTitle(title);

        const body = document.createElement("div");
        body.className = "report-content";
        appendContent(body, content);

        section.append(heading, body);
        finalReport.appendChild(section);
    });

    addDownloadButtons(normalizedReport);
    reportSection.hidden = false;
}

function appendContent(container, content) {
    if (content === null || content === undefined) {
        container.textContent = "N/A";
        return;
    }

    if (Array.isArray(content)) {
        const list = document.createElement("ul");

        content.forEach((item) => {
            const listItem = document.createElement("li");
            appendContent(listItem, item);
            list.appendChild(listItem);
        });

        container.appendChild(list);
        return;
    }

    if (typeof content === "object") {
        Object.entries(content).forEach(([key, value]) => {
            const label = document.createElement("strong");
            label.textContent = `${formatTitle(key)}: `;

            const row = document.createElement("p");
            row.append(label);

            const valueContainer = document.createElement("span");
            appendContent(valueContainer, value);

            row.appendChild(valueContainer);
            container.appendChild(row);
        });

        return;
    }

    container.textContent = String(content);
}

function addDownloadButtons(report) {
    const actions = document.createElement("div");
    actions.className = "report-actions";

    const markdownButton = document.createElement("button");
    markdownButton.type = "button";
    markdownButton.textContent = "Download Markdown";
    markdownButton.addEventListener("click", () => {
        downloadFile("prospect-report.md", reportToMarkdown(report), "text/markdown");
    });

    const pdfButton = document.createElement("button");
    pdfButton.type = "button";
    pdfButton.textContent = "Download PDF";
    pdfButton.addEventListener("click", () => downloadPdf());

    actions.append(markdownButton, pdfButton);
    finalReport.appendChild(actions);
}

function reportToMarkdown(report, level = 1) {
    let markdown = "";

    Object.entries(report).forEach(([key, value]) => {
        markdown += `${"#".repeat(level)} ${formatTitle(key)}\n\n`;

        if (value && typeof value === "object" && !Array.isArray(value)) {
            markdown += reportToMarkdown(value, level + 1);
        } else if (Array.isArray(value)) {
            markdown += value.map((item) => `- ${formatValue(item)}`).join("\n");
            markdown += "\n\n";
        } else {
            markdown += `${formatValue(value)}\n\n`;
        }
    });

    return markdown;
}


async function downloadPdf() {
    await loadPdfLibraries();

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF("p", "mm", "a4");

    const reportClone = finalReport.cloneNode(true);
    const actions = reportClone.querySelector(".report-actions");

    if (actions) {
        actions.remove();
    }

    const margin = 12;
    const pageWidth = 210;
    const pageHeight = 297;
    const contentWidth = pageWidth - margin * 2;
    const contentHeight = pageHeight - margin * 2;

    const temporaryContainer = document.createElement("div");

    Object.assign(temporaryContainer.style, {
        position: "fixed",
        left: "-10000px",
        top: "0",
        width: "794px",
        background: "#ffffff",
        color: "#172033",
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "14px",
        lineHeight: "1.5",
        boxSizing: "border-box",
        overflow: "visible"
    });

    Object.assign(reportClone.style, {
        display: "block",
        width: "100%",
        maxWidth: "none",
        minWidth: "0",
        height: "auto",
        margin: "0",
        padding: "24px",
        boxSizing: "border-box",
        background: "#ffffff",
        color: "#172033",
        overflow: "visible",
        whiteSpace: "normal",
        overflowWrap: "break-word",
        wordBreak: "normal"
    });

    reportClone.querySelectorAll("*").forEach((element) => {
        element.style.maxWidth = "100%";
        element.style.boxSizing = "border-box";
        element.style.whiteSpace = "normal";
        element.style.overflowWrap = "break-word";
        element.style.wordBreak = "normal";
        element.style.animation = "none";
        element.style.transition = "none";
    });

    reportClone.querySelectorAll(".report-card").forEach((card) => {
        Object.assign(card.style, {
            display: "block",
            width: "100%",
            height: "auto",
            margin: "0 0 24px 0",
            padding: "16px",
            background: "#ffffff",
            color: "#172033",
            overflow: "visible",
            border: "1px solid #e2e8f0",
            borderRadius: "6px",
            boxShadow: "none",
            breakInside: "auto",
            pageBreakInside: "auto"
        });
    });

    reportClone.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach(
        (heading) => {
            Object.assign(heading.style, {
                display: "block",
                width: "100%",
                height: "auto",
                margin: "0 0 12px 0",
                color: "#172033",
                fontSize: heading.tagName === "H3" ? "18px" : "16px",
                fontWeight: "700",
                lineHeight: "1.4",
                whiteSpace: "normal",
                overflowWrap: "break-word"
            });
        }
    );

    reportClone.querySelectorAll("p").forEach((paragraph) => {
        Object.assign(paragraph.style, {
            margin: "0 0 10px 0",
            lineHeight: "1.6",
            whiteSpace: "normal",
            overflowWrap: "break-word"
        });
    });

    reportClone.querySelectorAll("ul, ol").forEach((list) => {
        Object.assign(list.style, {
            display: "block",
            margin: "8px 0 12px 0",
            paddingLeft: "28px",
            listStylePosition: "outside"
        });
    });

    reportClone.querySelectorAll("li").forEach((item) => {
        Object.assign(item.style, {
            display: "list-item",
            margin: "0 0 8px 0",
            padding: "0",
            lineHeight: "1.6",
            whiteSpace: "normal",
            overflowWrap: "break-word"
        });
    });

    temporaryContainer.appendChild(reportClone);
    document.body.appendChild(temporaryContainer);

    try {
        await document.fonts.ready;

        const canvas = await window.html2canvas(reportClone, {
            scale: 2,
            useCORS: true,
            backgroundColor: "#ffffff",
            logging: false,
            width: reportClone.scrollWidth,
            height: reportClone.scrollHeight,
            windowWidth: reportClone.scrollWidth,
            windowHeight: reportClone.scrollHeight,
            scrollX: 0,
            scrollY: 0
        });

        const imageData = canvas.toDataURL("image/png");
        const imageHeight = (canvas.height * contentWidth) / canvas.width;

        let remainingHeight = imageHeight;
        let position = 0;

        pdf.addImage(
            imageData,
            "PNG",
            margin,
            margin,
            contentWidth,
            imageHeight,
            undefined,
            "FAST"
        );

        remainingHeight -= contentHeight;

        while (remainingHeight > 0) {
            position += contentHeight;
            pdf.addPage();

            pdf.addImage(
                imageData,
                "PNG",
                margin,
                margin - position,
                contentWidth,
                imageHeight,
                undefined,
                "FAST"
            );

            remainingHeight -= contentHeight;
        }

        pdf.save("prospect-report.pdf");
    } finally {
        temporaryContainer.remove();
    }
}

function downloadFile(filename, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
}

function renderMessage(message) {
    finalReport.replaceChildren();
    finalReport.textContent = message;
    reportSection.hidden = false;
}

function formatTitle(value) {
    return String(value)
        .replace(/_/g, " ")
        .replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatValue(value) {
    if (value === null || value === undefined) {
        return "N/A";
    }

    if (typeof value === "object") {
        return JSON.stringify(value);
    }

    return String(value);
}

function delay(milliseconds) {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function loadPdfLibraries() {
    const scripts = [];

    if (!window.jspdf) {
        scripts.push(
            loadScript(
                "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
            )
        );
    }

    if (!window.html2canvas) {
        scripts.push(
            loadScript(
                "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"
            )
        );
    }

    return Promise.all(scripts);
}

function loadScript(source) {
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = source;
        script.onload = resolve;
        script.onerror = () => reject(
            new Error(`Failed to load PDF library: ${source}`)
        );
        document.head.appendChild(script);
    });
}