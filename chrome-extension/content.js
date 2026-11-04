
function extractComments() {
    const threads = document.querySelectorAll(
        "ytd-comment-thread-renderer"
    );

    const comments = [];

    threads.forEach(thread => {
        const element = thread.querySelector("#content-text");
        const text = element?.innerText.trim();

        if (text) {
            comments.push(text);
        }
    });

    return comments;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "EXTRACT_COMMENTS") {
        const comments = extractComments();

        sendResponse({
            comments,
            total: comments.length
        });
    }
});
