$(document).ready(function () {
    let correctCount = 0;
    let wrongCount = 0;
    let totalCount = 0;
    let currentSubject = null;
    let currentClass = null;
    
    const subjects = {
        "9": ["All", "Chemistry", "Physics", "Biology", "Geography", "Civics", "History", "Economics", "Mathematics"],
        "10": ["All", "Chemistry", "Physics", "Biology", "Geography", "Political Science", "Economics", "History", "Mathematics"],
        "11": ["Accountancy Part-1", "Accountancy Part-2"],
        "12": ["Accountancy Part-1", "Accountancy Part-2"]
    };
    
    const $classDropdown = $("#class-dropdown");
    const $subjectDropdown = $("#subject-dropdown");
    const $classTitle = $classDropdown.find(".dropdown-title");
    const $subjectTitle = $subjectDropdown.find(".dropdown-title");
    
    $("#submit-answer").click(submitTextAnswer);
    $("#answer-input").keypress(function(e) {
        if (e.which === 13) submitTextAnswer();
    });
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
            loadQuestion('oneword', filename);
        });

        $subjectTitle.text($(this).text()).addClass("selected");
        $(".custom-dropdown").removeClass("open");

        if (currentClass && currentSubject) {
            loadQuestion('oneword', filename);
        } else {
            $("#question").text("Please select a class and subject.");
            $("#answer-box").hide();
            $("#result").hide();
            $("#explanation-box").hide();
        }
    });

    function loadQuestion(type, filename) {
        $("#question").text("Loading question...");
        $("#answer-box").hide();
        $("#explanation-box").hide();
        $("#result").text("");
        $("#explanation").text("");
        
        $.get(`/ask_question?type=${encodeURIComponent(type)}&file=${encodeURIComponent(filename)}`)
        .done(data => {
            if (data.question) {
                $("#question").text(data.question);
                $("#answer-box").show();
                $("#explanation-box").show();
                $("#answer-input").focus();
            } else {
                $("#question").text("Failed to load question. Try again.");
            }
        })
        .fail(() => {
            $("#question").text("Error loading question. Please try again.");
        });
    }

    function submitTextAnswer() {
        const userAnswer = $("#answer-input").val().trim().toLowerCase();
        if (!userAnswer) return
        
        totalCount++;
        const originalBorder = $("#answer-input").css('border-color');
        $("#answer-input").val('');
        
        $.ajax({
            url: "/check_answer",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ user_answer: userAnswer }),
            success: function(data) {
                if (data.result) {
                    if (data.result === "Correct") {
                        correctCount++;
                        $("#answer-input").css('border-color', 'green');
                    } else {
                        wrongCount++;
                        $("#answer-input").css('border-color', 'red');
                    }
                    updateCounters();
                    $("#result").text(data.result);
                    setTimeout(() => {
                        $("#answer-input").css('border-color', originalBorder);
                    }, 1000);
                    showExplanation();
                }
            }
        });
    }

    function showExplanation() {
        $.post("/show_explanation", function(data) {
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