// ================= FUTURE BUTTON =================

const futureButton = document.getElementById("futureButton");
const futureMessage = document.getElementById("futureMessage");

if (futureButton && futureMessage) {
    futureButton.addEventListener("click", function () {
        futureMessage.textContent =
            "The future of AI depends on how intelligently we build and use it.";
    });
}


// ================= NAVBAR SCROLL EFFECT =================

const navbar = document.querySelector(".navbar");

if (navbar) {
    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
}


// ================= SCROLL REVEAL =================

const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {
    revealElements.forEach(function (element) {
        const elementTop = element.getBoundingClientRect().top;

        if (elementTop < window.innerHeight - 100) {
            element.classList.add("active");
        }
    });
}

window.addEventListener("scroll", revealOnScroll);

revealOnScroll();


// ================= COUNTER ANIMATION =================

const counters = document.querySelectorAll(".counter");

counters.forEach(function (counter) {

    const target = Number(counter.dataset.target);

    if (Number.isNaN(target)) {
        return;
    }

    let current = 0;

    function updateCounter() {

        if (current < target) {

            current++;

            counter.textContent = current + "+";

            setTimeout(updateCounter, 30);

        } else {

            counter.textContent = target + "+";

        }
    }

    updateCounter();
});


// ================= AI TECHNOLOGY MODAL =================

const learnButtons = document.querySelectorAll(".learn-more");

const aiModal = document.getElementById("aiModal");
const closeModal = document.getElementById("closeModal");

const modalTitle = document.getElementById("modalTitle");
const modalDescription = document.getElementById("modalDescription");


const technologyInfo = {

    "Machine Learning":
        "Machine Learning allows computers to learn patterns from data and use those patterns to make predictions or decisions.",

    "Deep Learning":
        "Deep Learning uses multi-layer neural networks to process complex patterns in areas such as images, speech and language.",

    "Natural Language Processing":
        "Natural Language Processing helps computers understand, process and generate human language.",

    "Computer Vision":
        "Computer Vision enables computers to analyze and understand visual information such as images and videos."
};


if (
    aiModal &&
    modalTitle &&
    modalDescription
) {

    learnButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const topic =
                button.dataset.topic || "AI Technology";

            modalTitle.textContent = topic;

            modalDescription.textContent =
                technologyInfo[topic] ||
                "This AI technology is part of the AI Revolution project.";

            aiModal.classList.add("show");
        });
    });


    if (closeModal) {

        closeModal.addEventListener("click", function () {

            aiModal.classList.remove("show");

        });
    }


    aiModal.addEventListener("click", function (event) {

        if (event.target === aiModal) {

            aiModal.classList.remove("show");

        }
    });


    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            aiModal.classList.remove("show");

        }
    });
}


// ================= TEXT ANALYZER =================

// IMPORTANT:
// index.html uses id="textInput"

const analyzerText =
    document.getElementById("textInput");

const wordCount =
    document.getElementById("wordCount");

const characterCount =
    document.getElementById("characterCount");

const sentenceCount =
    document.getElementById("sentenceCount");

const readingTime =
    document.getElementById("readingTime");


if (
    analyzerText &&
    wordCount &&
    characterCount &&
    sentenceCount &&
    readingTime
) {

    function analyzeTextLive() {

        const text =
            analyzerText.value.trim();


        if (text === "") {

            wordCount.textContent = "0";

            characterCount.textContent = "0";

            sentenceCount.textContent = "0";

            readingTime.textContent = "0 min";

            return;
        }


        // Character Count

        const characters =
            text.length;


        // Word Count

        const words =
            text.split(/\s+/);

        const totalWords =
            words.length;


        // Sentence Count

        const sentences =
            text
                .split(/[.!?]+/)
                .filter(function (sentence) {
                    return sentence.trim() !== "";
                });

        const totalSentences =
            sentences.length;


        // Reading Time

        const wordsPerMinute = 200;

        const minutes =
            Math.max(
                1,
                Math.ceil(
                    totalWords / wordsPerMinute
                )
            );


        // Display

        wordCount.textContent =
            totalWords;

        characterCount.textContent =
            characters;

        sentenceCount.textContent =
            totalSentences;

        readingTime.textContent =
            minutes + " min";
    }


    // Live analysis while typing

    analyzerText.addEventListener(
        "input",
        analyzeTextLive
    );


    // Ctrl + Enter

    analyzerText.addEventListener(
        "keydown",
        function (event) {

            if (
                event.ctrlKey &&
                event.key === "Enter"
            ) {

                analyzeTextLive();

            }
        }
    );
}


// ================= AI CHAT =================

const chatInput =
    document.getElementById("chatInput");

const sendChatButton =
    document.getElementById("sendChatButton");

const chatMessages =
    document.getElementById("chatMessages");

const clearChatButton =
    document.getElementById("clearChatButton");


if (
    chatInput &&
    sendChatButton &&
    chatMessages &&
    clearChatButton
) {


    // ================= ADD USER MESSAGE =================

    function addUserMessage(message) {

        const div =
            document.createElement("div");

        div.className =
            "user-message";


        const name =
            document.createElement("span");

        name.className =
            "message-name";

        name.textContent =
            "You";


        const paragraph =
            document.createElement("p");

        paragraph.textContent =
            message;


        div.appendChild(name);

        div.appendChild(paragraph);

        chatMessages.appendChild(div);


        chatMessages.scrollTop =
            chatMessages.scrollHeight;
    }


    // ================= ADD BOT MESSAGE =================

    function addBotMessage(message) {

        const div =
            document.createElement("div");

        div.className =
            "bot-message";


        const name =
            document.createElement("span");

        name.className =
            "message-name";

        name.textContent =
            "AI Assistant";


        const paragraph =
            document.createElement("p");

        paragraph.textContent =
            message;


        div.appendChild(name);

        div.appendChild(paragraph);

        chatMessages.appendChild(div);


        chatMessages.scrollTop =
            chatMessages.scrollHeight;
    }


    // ================= GET CSRF TOKEN =================

    function getCSRFToken() {

        const csrfInput =
            document.querySelector(
                '[name="csrfmiddlewaretoken"]'
            );

        if (csrfInput) {
            return csrfInput.value;
        }


        // Fallback: cookie

        const cookies =
            document.cookie.split(";");


        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (
                cookie.startsWith("csrftoken=")
            ) {

                return decodeURIComponent(
                    cookie.substring(
                        "csrftoken=".length
                    )
                );
            }
        }

        return "";
    }


    // ================= SEND MESSAGE =================

    async function sendMessage() {

        const message =
            chatInput.value.trim();


        if (
            message === "" ||
            sendChatButton.disabled
        ) {

            return;
        }


        // Add user message

        addUserMessage(message);


        // Clear input

        chatInput.value = "";


        // Loading state

        chatInput.disabled = true;

        sendChatButton.disabled = true;

        sendChatButton.textContent = "...";


        // Thinking message

        const thinkingMessage =
            document.createElement("div");

        thinkingMessage.className =
            "bot-message";


        const thinkingName =
            document.createElement("span");

        thinkingName.className =
            "message-name";

        thinkingName.textContent =
            "AI Assistant";


        const thinkingText =
            document.createElement("p");

        thinkingText.textContent =
            "Thinking...";


        thinkingMessage.appendChild(
            thinkingName
        );

        thinkingMessage.appendChild(
            thinkingText
        );


        chatMessages.appendChild(
            thinkingMessage
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;


        // ================= DJANGO API =================

        const formData =
            new FormData();

        formData.append(
            "message",
            message
        );


        try {

            const response =
                await fetch(
                    "/api/chat/",
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken":
                                getCSRFToken()
                        },

                        body: formData
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Server returned an error."
                );
            }


            const data =
                await response.json();


            // Remove thinking

            thinkingMessage.remove();


            // Show AI response

            addBotMessage(
                data.reply ||
                "Sorry, I could not generate a response."
            );


        } catch (error) {

            console.error(
                "Chat Error:",
                error
            );


            thinkingMessage.remove();


            addBotMessage(
                "Sorry, something went wrong while connecting to the AI server."
            );

        } finally {

            chatInput.disabled = false;

            sendChatButton.disabled = false;

            sendChatButton.textContent =
                "Send";

            chatInput.focus();
        }
    }


    // ================= SEND BUTTON =================

    sendChatButton.addEventListener(
        "click",
        sendMessage
    );


    // ================= ENTER KEY =================

    chatInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();

                sendMessage();
            }
        }
    );


    // ================= CLEAR CHAT =================

    clearChatButton.addEventListener(
        "click",
        function () {

            chatMessages.innerHTML = `
                <div class="bot-message">

                    <span class="message-name">
                        AI Assistant
                    </span>

                    <p>
                        Chat cleared. How can I help you?
                    </p>

                </div>
            `;

            chatInput.focus();
        }
    );
}


// ================= AI DASHBOARD CLOCK =================

const currentTime =
    document.getElementById("currentTime");


function updateClock() {

    if (!currentTime) {
        return;
    }


    const now =
        new Date();


    const hours =
        String(
            now.getHours()
        ).padStart(2, "0");


    const minutes =
        String(
            now.getMinutes()
        ).padStart(2, "0");


    const seconds =
        String(
            now.getSeconds()
        ).padStart(2, "0");


    currentTime.textContent =
        hours +
        ":" +
        minutes +
        ":" +
        seconds;
}


if (currentTime) {

    updateClock();

    setInterval(
        updateClock,
        1000
    );
}


// ================= TECHNOLOGY PROGRESS =================

const progressBars =
    document.querySelectorAll(
        ".progress-fill"
    );

let progressAnimated = false;


function animateProgressBars() {

    if (
        progressAnimated ||
        progressBars.length === 0
    ) {

        return;
    }


    progressBars.forEach(
        function (bar) {

            const progress =
                Number(
                    bar.dataset.progress
                );


            if (
                !Number.isNaN(progress)
            ) {

                const safeProgress =
                    Math.max(
                        0,
                        Math.min(
                            100,
                            progress
                        )
                    );


                bar.style.width =
                    safeProgress + "%";
            }
        }
    );


    progressAnimated = true;
}


function checkProgressBars() {

    if (
        progressAnimated ||
        progressBars.length === 0
    ) {

        return;
    }


    const dashboard =
        document.getElementById(
            "dashboard"
        );


    if (!dashboard) {

        animateProgressBars();

        return;
    }


    const dashboardTop =
        dashboard.getBoundingClientRect().top;


    if (
        dashboardTop <
        window.innerHeight - 150
    ) {

        animateProgressBars();
    }
}


window.addEventListener(
    "scroll",
    checkProgressBars
);


window.addEventListener(
    "load",
    checkProgressBars
);


checkProgressBars();


// ================= SCRIPT LOADED =================

console.log(
    "AI-Revolution script loaded successfully."
);