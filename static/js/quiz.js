$(document).ready(function () {
    let correctCount = 0;
    let wrongCount = 0;
    let totalCount = 0;
    let currentSubject = null;
    let currentClass = null;
    
    const subjects = {
        "9": ["All", "Chemistry", "Physics", "Biology", "Geography", "Civics", "History", "Economics"],
        "10": ["All", "Chemistry", "Physics", "Biology", "Geography", "Political Science", "Economics", "History"]
        // "11": ["Chemistry", "Physics", "Biology", "Accountancy", "Business Studies", "Economics", "Political Science", "Geography", "History", "Computer Science"],
        // "12": ["Chemistry", "Physics", "Biology", "Accountancy", "Business Studies", "Economics", "Political Science", "Geography", "History", "Computer Science"]
    };
    
    const $classDropdown = $("#class-dropdown");
    const $subjectDropdown = $("#subject-dropdown");
    const $classTitle = $classDropdown.find(".dropdown-title");
    const $subjectTitle = $subjectDropdown.find(".dropdown-title");
    
    $("#true-answer").click(() => submitAnswer(true));
    $("#false-answer").click(() => submitAnswer(false));
    $("#show-explanation").click(showExplanation);
    
    $classDropdown.click(function (e) {
        e.stopPropagation();
        $(this).toggleClass("open");
        $subjectDropdown.removeClass("open");
    });

    $subjectDropdown.click(function (e) {
        if ($(this).hasClass("disabled")) return;
        e.stopPropagation();
        $(this).toggleClass("open");
        $classDropdown.removeClass("open");
    });

    $(document).click(() => {
        $(".custom-dropdown").removeClass("open");
    });
    
    $("#question").text("Please select a class and subject.");
    $("#answer-box").hide();
    $("#explanation-box").hide();
    
    $classDropdown.on("click", ".dropdown-item", function (e) {
        e.stopPropagation();
        currentClass = $(this).data("value");
        $classTitle.text($(this).text()).addClass("selected");
        
        currentSubject = null;
        $subjectTitle.text("Select Subject").removeClass("selected");
        $("#question").text("Please select a class and subject.");
        $("#answer-box").hide();
        $("#explanation-box").hide();
        
        $subjectDropdown.removeClass("disabled")
        .find(".dropdown-items")
        .html(subjects[currentClass].map(subj =>
            `<div class="dropdown-item" data-value="${subj}">${subj}</div>`
        ).join(""));
        
        $subjectDropdown.addClass("open");
        $classDropdown.removeClass("open");
    });
    
    $subjectDropdown.on("click", ".dropdown-item", function (e) {
        e.stopPropagation();
        const rawSubject = $(this).data("value");
        currentSubject = rawSubject;

        const formattedSubject = rawSubject.toLowerCase().replace(/ /g, '_');
        const filename = `${formattedSubject}${currentClass}.json`;

        $("#next-question").off("click").click(() => {
            $("#result").text("");
            $("#explanation").text("");
            $("#explanation-box").hide();
            loadQuestion(filename);
        });

        $subjectTitle.text($(this).text()).addClass("selected");
        $(".custom-dropdown").removeClass("open");

        if (currentClass && currentSubject) {
            loadQuestion(filename);
        } else {
            $("#question").text("Please select a class and subject.");
            $("#answer-box").hide();
            $("#result").hide();
            $("#explanation-box").hide();
        }
    });

    function loadQuestion(filename) {
        $("#question").text("Loading question...");
        $("#answer-box").hide();
        $("#explanation-box").hide();
        $("#result").text("");
        $("#explanation").text("");
        
        $.get(`/ask_question?file=${encodeURIComponent(filename)}`)
        .done(data => {
            if (data.question) {
                $("#question").text(data.question);
                $("#answer-box").show();
                $("#explanation-box").show();
            } else {
                $("#question").text("Failed to load question. Try again.");
            }
        })
        .fail(() => {
            $("#question").text("Error loading question. Please try again.");
        });
    }

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
                }
            }
        });
    }

    function showExplanation() {
        $.post("/show_explanation", function (data) {
            if (data.explanation) {
                $("#explanation").text(data.explanation);
            }
        });
    }

    function updateCounters() {
        $("#correct-count").text(correctCount);
        $("#wrong-count").text(wrongCount);
        $("#total-count").text(totalCount);
    }
});