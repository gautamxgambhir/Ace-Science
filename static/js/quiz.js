$(document).ready(function () {
    let correctCount = 0;
    let wrongCount = 0;
    let totalCount = 0;

    // Load the first question
    loadQuestion();

    // Handle True button click
    $("#true-answer").click(function () {
        submitAnswer(true);
    });

    // Handle False button click
    $("#false-answer").click(function () {
        submitAnswer(false);
    });

    // Handle Next Question button click
    $("#next-question").click(function () {
        loadQuestion();
    });
    $("#show-explanation").click(function () {
        showExplanation();
    });

    // Function to load a new question
    function loadQuestion() {
        $.get("/ask_question", function (data) {
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
