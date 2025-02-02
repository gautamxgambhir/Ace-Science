$(document).ready(function () {
    let correctCount = 0;
    let wrongCount = 0;
    let totalCount = 0;
    let currentSubject = null;

    // Load first question
    loadQuestion();

    // Subject selection handler
    $("#subject-dropdown").change(function () {
        currentSubject = $(this).val();
        if (currentSubject) {
            sessionStorage.setItem('selectedSubject', currentSubject); // Store subject
            loadQuestion(currentSubject);
        }
    });

    // Button handlers
    $("#true-answer").click(() => submitAnswer(true));
    $("#false-answer").click(() => submitAnswer(false));
    $("#next-question").click(() => loadQuestion(currentSubject));
    $("#show-explanation").click(showExplanation);

    // Modified loadQuestion function
    function loadQuestion(subject = null) {
        let url = "/ask_question";
        if (subject) {
            url += `?subject=${encodeURIComponent(subject)}`;
        }

        $.get(url, function (data) {
            if (data.question) {
                $("#question").text(data.question);
                $("#result").text("");
                $("#explanation").text("");
            } else {
                $("#question").text("Failed to load question. Try again.");
            }
        });
    }

    // Function to submit the answer
    function submitAnswer(answer) {
        totalCount++;
        $.ajax({
            url: "/check_answer",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ user_answer: answer }),
            success: function (data) {
                if (data.result) {
                    if (data.result === "Correct") {
                        correctCount++;
                    } else {
                        wrongCount++;
                    }
                    updateCounters();
                    $("#result").text(data.result);
                    showExplanation();
                } else {
                    $("#result").text("Error checking answer. Try again.");
                }
            },
            error: function () {
                $("#result").text("Error submitting answer. Please try again.");
            }
        });
    }

    // Function to show the explanation
    function showExplanation() {
        $.post("/show_explanation", function (data) {
            if (data.explanation) {
                $("#explanation").text(data.explanation);
            } else {
                $("#explanation").text("No explanation available.");
            }
        });
    }

    // Function to update counters
    function updateCounters() {
        $("#correct-count").text(correctCount);
        $("#wrong-count").text(wrongCount);
        $("#total-count").text(totalCount);
    }
});