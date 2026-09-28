let currentFileId = null;
let currentReport = null;


/* =====================================================
   CONFIGURATION
   ===================================================== */

const AUTH_ENDPOINT =
    "/api/auth/login";

const REGISTER_ENDPOINT =
    "/api/auth/register";

const ANALYZE_ENDPOINT =
    "/api/analyze";

const CHAT_ENDPOINT =
    "/api/chat";


/* =====================================================
   INITIALIZATION
   ===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);


function initializeApplication() {

    const loginForm =
        getElement("loginForm");

    const logoutButton =
        getElement("logoutButton");

    const registerForm =
        getElement("registerForm");

    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            handleLogin
        );

    }

    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            logout
        );

    }

    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            handleRegistration
        );

    }

    initializeUpload();
    initializeChat();

    const token = getToken();

    if (token) {

        showApplication();

    } else {

        showLogin();

    }
}


/* =====================================================
   ELEMENT
   ===================================================== */

function getElement(id) {

    return document.getElementById(id);

}


/* =====================================================
   TOKEN
   ===================================================== */

function getToken() {

    return localStorage.getItem(
        "access_token"
    );

}


function saveToken(token) {

    localStorage.setItem(
        "access_token",
        token
    );

}


function clearToken() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "username"
    );

    localStorage.removeItem(
        "user_role"
    );

    localStorage.removeItem(
        "user_id"
    );

}


/* =====================================================
   LOGIN SCREEN
   ===================================================== */

function showLogin() {

    const loginScreen =
        getElement("loginScreen");

    const appScreen =
        getElement("appScreen");

    if (loginScreen) {

        loginScreen.classList.remove(
            "hidden"
        );

    }

    if (appScreen) {

        appScreen.classList.add(
            "hidden"
        );

    }

}


function showApplication() {

    const loginScreen =
        getElement("loginScreen");

    const appScreen =
        getElement("appScreen");

    if (loginScreen) {

        loginScreen.classList.add(
            "hidden"
        );

    }

    if (appScreen) {

        appScreen.classList.remove(
            "hidden"
        );

    }

    updateUserInterface();

}


/* =====================================================
   LOGIN
   ===================================================== */

async function handleLogin(event) {

    event.preventDefault();

    const usernameInput =
        getElement("username");

    const passwordInput =
        getElement("password");

    const loginButton =
        getElement("loginButton");

    const loginMessage =
        getElement("loginMessage");

    const username =
        usernameInput.value.trim();

    const password =
        passwordInput.value;

    if (!username || !password) {

        loginMessage.textContent =
            "Please enter username and password.";

        return;

    }

    loginButton.disabled = true;

    loginButton.textContent =
        "Logging in...";

    loginMessage.textContent =
        "";

    try {

        const response =
            await fetch(
                AUTH_ENDPOINT,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username: username,
                        password: password
                    })

                }
            );

        const data =
            await parseResponse(
                response
            );

        if (!response.ok) {

            throw new Error(
                getApiErrorMessage(
                    data,
                    "Login failed."
                )
            );

        }

        if (!data.access_token) {

            throw new Error(
                "Server did not return an access token."
            );

        }

        saveToken(
            data.access_token
        );

        localStorage.setItem(
            "username",
            data.username || username
        );

        localStorage.setItem(
            "user_role",
            data.role || "analyst"
        );

        localStorage.setItem(
            "user_id",
            String(
                data.user_id || ""
            )
        );

        currentFileId = null;
        currentReport = null;

        passwordInput.value = "";

        loginMessage.textContent =
            "";

        showApplication();

    } catch (error) {

        console.error(
            "LOGIN ERROR:",
            error
        );

        loginMessage.textContent =
            error.message ||
            "Login failed.";

    } finally {

        loginButton.disabled =
            false;

        loginButton.textContent =
            "Login";

    }

}


/* =====================================================
   USER UI
   ===================================================== */

function updateUserInterface() {

    const username =
        localStorage.getItem(
            "username"
        ) || "User";

    const role =
        localStorage.getItem(
            "user_role"
        ) || "analyst";

    const usernameElement =
        getElement(
            "loggedUsername"
        );

    const roleElement =
        getElement(
            "loggedRole"
        );

    const initialElement =
        getElement(
            "userInitial"
        );

    if (usernameElement) {

        usernameElement.textContent =
            username;

    }

    if (roleElement) {

        roleElement.textContent =
            role;

    }

    if (initialElement) {

        initialElement.textContent =
            username
                .charAt(0)
                .toUpperCase();

    }


    const adminSection =
        getElement(
            "adminSection"
        );

    const adminNav =
        getElement(
            "adminNav"
        );

    if (role === "admin") {

        if (adminSection) {

            adminSection.classList.remove(
                "hidden"
            );

        }

        if (adminNav) {

            adminNav.classList.remove(
                "hidden"
            );

        }

    } else {

        if (adminSection) {

            adminSection.classList.add(
                "hidden"
            );

        }

        if (adminNav) {

            adminNav.classList.add(
                "hidden"
            );

        }

    }

}


/* =====================================================
   LOGOUT
   ===================================================== */

function logout() {

    clearToken();

    currentFileId = null;

    currentReport = null;

    const reportSection =
        getElement(
            "reportSection"
        );

    const uploadSection =
        getElement(
            "uploadSection"
        );

    const investigationInfo =
        getElement(
            "investigationInfo"
        );

    const chatMessages =
        getElement(
            "chatMessages"
        );

    if (reportSection) {

        reportSection.classList.add(
            "hidden"
        );

    }

    if (uploadSection) {

        uploadSection.classList.remove(
            "hidden"
        );

    }

    if (investigationInfo) {

        investigationInfo.textContent =
            "No investigation loaded.";

    }

    if (chatMessages) {

        chatMessages.innerHTML =
            "";

    }

    showLogin();

}


/* =====================================================
   ADMIN REGISTRATION
   ===================================================== */

async function handleRegistration(event) {

    event.preventDefault();

    const token =
        getToken();

    if (!token) {

        handleUnauthorized();

        return;

    }

    const username =
        getElement(
            "newUsername"
        ).value.trim();

    const email =
        getElement(
            "newEmail"
        ).value.trim();

    const fullName =
        getElement(
            "newFullName"
        ).value.trim();

    const password =
        getElement(
            "newPassword"
        ).value;

    const department =
        getElement(
            "newDepartment"
        ).value.trim();

    const role =
        getElement(
            "newRole"
        ).value;

    const button =
        getElement(
            "registerButton"
        );

    const message =
        getElement(
            "registerMessage"
        );

    button.disabled =
        true;

    button.textContent =
        "Creating...";

    message.textContent =
        "";

    message.className =
        "register-message";

    try {

        const response =
            await fetch(
                REGISTER_ENDPOINT,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body: JSON.stringify({

                        username:
                            username,

                        email:
                            email,

                        full_name:
                            fullName,

                        password:
                            password,

                        role:
                            role,

                        department:
                            department ||
                            null

                    })

                }
            );

        if (
            response.status === 401
        ) {

            handleUnauthorized();

            return;

        }

        const data =
            await parseResponse(
                response
            );

        if (!response.ok) {

            throw new Error(
                getApiErrorMessage(
                    data,
                    "User creation failed."
                )
            );

        }

        message.textContent =
            `User "${data.username}" created successfully.`;

        message.classList.add(
            "success"
        );

        getElement(
            "registerForm"
        ).reset();

    } catch (error) {

        console.error(
            "REGISTRATION ERROR:",
            error
        );

        message.textContent =
            error.message;

        message.classList.add(
            "error"
        );

    } finally {

        button.disabled =
            false;

        button.textContent =
            "Create User";

    }

}


/* =====================================================
   UPLOAD
   ===================================================== */

function initializeUpload() {

    const fileInput =
        getElement(
            "fileInput"
        );

    if (!fileInput) {

        return;

    }

    fileInput.addEventListener(
        "change",
        async function () {

            const file =
                fileInput.files[0];

            if (!file) {

                return;

            }

            await uploadFile(
                file
            );

            fileInput.value =
                "";

        }
    );

}


async function uploadFile(file) {

    const token =
        getToken();

    if (!token) {

        showLogin();

        return;

    }

    const statusElement =
        getElement(
            "status"
        );

    const uploadMessage =
        getElement(
            "uploadMessage"
        );

    if (statusElement) {

        statusElement.textContent =
            "Analyzing...";

    }

    if (uploadMessage) {

        uploadMessage.textContent =
            "Uploading and analyzing the file...";

    }

    const allowedExtensions = [
        ".log",
        ".csv",
        ".xlsx"
    ];

    const fileName =
        file.name.toLowerCase();

    const valid =
        allowedExtensions.some(
            extension =>
                fileName.endsWith(
                    extension
                )
        );

    if (!valid) {

        if (statusElement) {

            statusElement.textContent =
                "Error";

        }

        if (uploadMessage) {

            uploadMessage.textContent =
                "Unsupported file type. Use .log, .csv or .xlsx.";

        }

        return;

    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    try {

        const response =
            await fetch(
                ANALYZE_ENDPOINT,
                {

                    method: "POST",

                    headers: {

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body:
                        formData

                }
            );

        if (
            response.status === 401
        ) {

            handleUnauthorized();

            return;

        }

        const data =
            await parseResponse(
                response
            );

        if (!response.ok) {

            throw new Error(
                getApiErrorMessage(
                    data,
                    "Analysis failed."
                )
            );

        }

        currentFileId =
            data.file_id;

        currentReport =
            data.report;

        displayReport(
            data.report || {}
        );

        const investigationInfo =
            getElement(
                "investigationInfo"
            );

        if (investigationInfo) {

            investigationInfo.innerHTML =
                `
                <strong>
                    ${escapeHtml(
                        file.name
                    )}
                </strong>
                <br>
                ID:
                ${escapeHtml(
                    data.file_id || "-"
                )}
                `;

        }

        if (statusElement) {

            statusElement.textContent =
                "Completed";

        }

        if (uploadMessage) {

            uploadMessage.textContent =
                "Analysis completed successfully.";

        }

    } catch (error) {

        console.error(
            "UPLOAD ERROR:",
            error
        );

        if (statusElement) {

            statusElement.textContent =
                "Error";

        }

        if (uploadMessage) {

            uploadMessage.textContent =
                error.message ||
                "Analysis failed.";

        }

    }

}


/* =====================================================
   UNAUTHORIZED
   ===================================================== */

function handleUnauthorized() {

    clearToken();

    currentFileId = null;

    currentReport = null;

    showLogin();

    const message =
        getElement(
            "loginMessage"
        );

    if (message) {

        message.textContent =
            "Session expired. Please log in again.";

    }

}


/* =====================================================
   CHAT
   ===================================================== */

function initializeChat() {

    const button =
        getElement(
            "chatButton"
        );

    const input =
        getElement(
            "chatInput"
        );

    if (button) {

        button.addEventListener(
            "click",
            sendChat
        );

    }

    if (input) {

        input.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter"
                ) {

                    event.preventDefault();

                    sendChat();

                }

            }
        );

    }

}


async function sendChat() {

    const input =
        getElement(
            "chatInput"
        );

    if (!input) {

        return;

    }

    const question =
        input.value.trim();

    if (!question) {

        return;

    }

    if (!currentFileId) {

        addChatMessage(
            "Please analyze a log before asking questions.",
            "ai"
        );

        return;

    }

    const token =
        getToken();

    if (!token) {

        handleUnauthorized();

        return;

    }

    addChatMessage(
        question,
        "user"
    );

    input.value =
        "";

    addChatMessage(
        "Analyzing your question...",
        "ai",
        true
    );

    try {

        const response =
            await fetch(
                CHAT_ENDPOINT,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body: JSON.stringify({

                        file_id:
                            currentFileId,

                        question:
                            question

                    })

                }
            );

        if (
            response.status === 401
        ) {

            handleUnauthorized();

            return;

        }

        const data =
            await parseResponse(
                response
            );

        if (!response.ok) {

            throw new Error(
                getApiErrorMessage(
                    data,
                    "Chat failed."
                )
            );

        }

        removeLoadingChatMessage();

        addChatMessage(
            data.answer ||
            "No answer returned.",
            "ai"
        );

    } catch (error) {

        removeLoadingChatMessage();

        addChatMessage(
            "Error: " +
            (
                error.message ||
                "Unable to answer."
            ),
            "ai"
        );

    }

}


/* =====================================================
   CHAT MESSAGE
   ===================================================== */

function addChatMessage(
    message,
    type,
    loading = false
) {

    const container =
        getElement(
            "chatMessages"
        );

    if (!container) {

        return;

    }

    const element =
        document.createElement(
            "div"
        );

    element.className =
        "chat-message " +
        (
            type === "user"
                ? "chat-user"
                : "chat-ai"
        );

    if (loading) {

        element.classList.add(
            "chat-loading"
        );

    }

    element.textContent =
        message;

    container.appendChild(
        element
    );

    container.scrollTop =
        container.scrollHeight;

}


function removeLoadingChatMessage() {

    const container =
        getElement(
            "chatMessages"
        );

    if (!container) {

        return;

    }

    const loading =
        container.querySelector(
            ".chat-loading"
        );

    if (loading) {

        loading.remove();

    }

}


/* =====================================================
   REPORT
   ===================================================== */

function displayReport(report) {

    const uploadSection =
        getElement(
            "uploadSection"
        );

    const reportSection =
        getElement(
            "reportSection"
        );

    if (uploadSection) {

        uploadSection.classList.add(
            "hidden"
        );

    }

    if (reportSection) {

        reportSection.classList.remove(
            "hidden"
        );

    }

    const rca =
        report.rca || {};

    const incident =
        getElement("incident");

    if (incident) {

        incident.textContent =
            report.incident ||
            "Incident not determined.";

    }

    const summary =
        getElement("summary");

    if (summary) {

        summary.textContent =
            report.summary ||
            "No summary available.";

    }

    const rootCause =
        getElement("rootCause");

    if (rootCause) {

        rootCause.textContent =
            rca.potential_root_cause ||
            "Not determined.";

    }

    const reasoning =
        getElement("reasoning");

    if (reasoning) {

        reasoning.textContent =
            rca.reasoning ||
            "No reasoning available.";

    }

    const confidence =
        getElement("confidence");

    if (confidence) {

        confidence.textContent =
            formatConfidence(
                rca.confidence
            );

    }

    const findings =
        Array.isArray(
            report.findings
        )
            ? report.findings
            : [];

    const evidence =
        Array.isArray(
            report.evidence
        )
            ? report.evidence
            : [];

    const findingCount =
        getElement(
            "findingCount"
        );

    if (findingCount) {

        findingCount.textContent =
            findings.length;

    }

    const evidenceCount =
        getElement(
            "evidenceCount"
        );

    if (evidenceCount) {

        evidenceCount.textContent =
            evidence.length;

    }

    const severity =
        getElement(
            "severity"
        );

    if (severity) {

        severity.textContent =
            getHighestSeverity(
                findings
            );

    }

    displayFindings(
        findings
    );

    displayEvidence(
        evidence
    );

    displayRecommendations(
        Array.isArray(
            report.recommendations
        )
            ? report.recommendations
            : []
    );

    displayLimitations(
        Array.isArray(
            report.limitations
        )
            ? report.limitations
            : []
    );

}


/* =====================================================
   FINDINGS
   ===================================================== */

function displayFindings(
    findings
) {

    const container =
        getElement(
            "findings"
        );

    if (!container) {

        return;

    }

    container.innerHTML =
        "";

    if (!findings.length) {

        container.innerHTML =
            "<p>No findings.</p>";

        return;

    }

    findings.forEach(
        function (finding) {

            const element =
                document.createElement(
                    "div"
                );

            element.className =
                "finding";

            element.innerHTML =
                `
                <div class="finding-title">
                    ${escapeHtml(
                        finding.title ||
                        "Untitled finding"
                    )}
                </div>

                <span class="badge">
                    ${escapeHtml(
                        finding.category ||
                        "unknown"
                    )}
                </span>

                <span class="badge">
                    Severity:
                    ${escapeHtml(
                        finding.severity ||
                        "LOW"
                    )}
                </span>

                <span class="badge">
                    Confidence:
                    ${formatConfidence(
                        finding.confidence
                    )}
                </span>

                <p>
                    ${escapeHtml(
                        finding.description ||
                        ""
                    )}
                </p>
                `;

            container.appendChild(
                element
            );

        }
    );

}


/* =====================================================
   EVIDENCE
   ===================================================== */

function displayEvidence(
    evidence
) {

    const container =
        getElement(
            "evidence"
        );

    if (!container) {

        return;

    }

    container.innerHTML =
        "";

    if (!evidence.length) {

        container.innerHTML =
            "<p>No evidence available.</p>";

        return;

    }

    evidence.forEach(
        function (item) {

            const element =
                document.createElement(
                    "div"
                );

            element.className =
                "evidence-item";

            const source =
                item.source ||
                item.reference ||
                item.source_file ||
                item.type ||
                "Unknown";

            const content =
                item.content ||
                item.raw_log ||
                item.message ||
                "";

            let lineInfo =
                "";

            if (
                item.line_start !==
                undefined &&
                item.line_start !==
                null
            ) {

                if (
                    item.line_end !==
                    undefined &&
                    item.line_end !==
                    null
                ) {

                    lineInfo =
                        `Lines ${item.line_start}-${item.line_end}`;

                } else {

                    lineInfo =
                        `Line ${item.line_start}`;

                }

            }

            element.innerHTML =
                `
                <div class="evidence-source">

                    ${escapeHtml(
                        source
                    )}

                    ${
                        lineInfo
                            ? " — " +
                              escapeHtml(
                                  lineInfo
                              )
                            : ""
                    }

                </div>

                <div class="evidence-content">

                    ${escapeHtml(
                        content
                    )}

                </div>
                `;

            container.appendChild(
                element
            );

        }
    );

}


/* =====================================================
   RECOMMENDATIONS
   ===================================================== */

function displayRecommendations(
    recommendations
) {

    const container =
        getElement(
            "recommendations"
        );

    if (!container) {

        return;

    }

    container.innerHTML =
        "";

    if (!recommendations.length) {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            "No recommendations available.";

        container.appendChild(
            li
        );

        return;

    }

    recommendations.forEach(
        function (item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

            container.appendChild(
                li
            );

        }
    );

}


/* =====================================================
   LIMITATIONS
   ===================================================== */

function displayLimitations(
    limitations
) {

    const container =
        getElement(
            "limitations"
        );

    if (!container) {

        return;

    }

    container.innerHTML =
        "";

    if (!limitations.length) {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            "No limitations reported.";

        container.appendChild(
            li
        );

        return;

    }

    limitations.forEach(
        function (item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

            container.appendChild(
                li
            );

        }
    );

}


/* =====================================================
   API RESPONSE
   ===================================================== */

async function parseResponse(
    response
) {

    const contentType =
        response.headers.get(
            "content-type"
        ) || "";

    if (
        contentType.includes(
            "application/json"
        )
    ) {

        try {

            return await response.json();

        } catch {

            return {
                detail:
                    "Server returned invalid JSON."
            };

        }

    }

    try {

        const text =
            await response.text();

        return {
            detail:
                text ||
                "Server returned an empty response."
        };

    } catch {

        return {
            detail:
                "Unable to read server response."
        };

    }

}


/* =====================================================
   API ERROR
   ===================================================== */

function getApiErrorMessage(
    data,
    fallback
) {

    if (!data) {

        return fallback;

    }

    if (
        typeof data.detail ===
        "string"
    ) {

        return data.detail;

    }

    if (
        Array.isArray(
            data.detail
        )
    ) {

        return data.detail
            .map(
                item =>
                    item?.msg ||
                    JSON.stringify(item)
            )
            .join(", ");

    }

    if (data.detail) {

        return JSON.stringify(
            data.detail
        );

    }

    if (data.message) {

        return data.message;

    }

    return fallback;

}


/* =====================================================
   CONFIDENCE
   ===================================================== */

function formatConfidence(
    confidence
) {

    if (
        confidence === undefined ||
        confidence === null
    ) {

        return "-";

    }

    const value =
        Number(
            confidence
        );

    if (
        Number.isNaN(
            value
        )
    ) {

        return "-";

    }

    return (
        value * 100
    ).toFixed(0) + "%";

}


/* =====================================================
   SEVERITY
   ===================================================== */

function getHighestSeverity(
    findings
) {

    const levels = {

        CRITICAL: 4,
        HIGH: 3,
        MEDIUM: 2,
        LOW: 1

    };

    let highest =
        "LOW";

    findings.forEach(
        function (finding) {

            const severity =
                String(
                    finding.severity ||
                    "LOW"
                ).toUpperCase();

            if (
                (levels[severity] || 1) >
                (levels[highest] || 1)
            ) {

                highest =
                    severity;

            }

        }
    );

    return highest;

}


/* =====================================================
   ESCAPE HTML
   ===================================================== */

function escapeHtml(
    value
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        String(
            value ?? ""
        );

    return div.innerHTML;

}