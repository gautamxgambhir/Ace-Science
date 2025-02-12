$(document).ready(function () {
    let correctCount = 0;
    let wrongCount = 0;
    let totalCount = 0;
    let currentSubject = null;
    let currentClass = null;
    
    const subjects = {
        "9": {
            "All": "all9.json",
            "Chemistry": "chemistry9.json",
            "Physics": "physics9.json",
            "Biology": "biology9.json",
            "Geography": "geography9.json",
            "Civics": "civics9.json",
            "History": "history9.json",
            "Economics": "economics9.json",
            "Mathematics": "mathematics9.json"
        },
        "10": {
            "All": "all10.json",
            "Chemistry": "chemistry10.json",
            "Physics": "physics10.json",
            "Biology": "biology10.json",
            "Geography": "geography10.json",
            "Political Science": "political_science10.json",
            "Economics": "economics10.json",
            "History": "history10.json",
            "Mathematics": "mathematics10.json",
            "English communicative": "english_communicative10.json",
        },
        "11": {
            "Accountancy Part-1": "accountancy_part1_11.json",
            "Accountancy Part-2": "accountancy_part2_11.json",
            "Business Studies": "business_studies_11.json",
            "Statistics for Economics": "economics_statistics_11.json",
            "Indian Economic Development":"indian_economic_development_11.json",
            "Mathematics":"mathematics_11.json",
        },
        "12": {
            "Accountancy Part-1": "accountancy_part1_12.json",
            "Accountancy Part-2": "accountancy_part2_12.json",
            "Business Studies Part-1": "business_studies_part1_12.json",
            "Business Studies Part-2": "business_studies_part2_12.json",
            "Microeconomics": "microeconomics_12.json",
            "Macroeconomics": "macroeconomics_12.json",
            "Mathematics Part-1":"mathematics_part1_12.json",
            "Mathematics Part-2":"mathematics_part2_12.json",
        }
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
        .html(Object.keys(subjects[currentClass]).map(subj =>
            `<div class="dropdown-item" data-value="${subj}">${subj}</div>`
        ).join(""));
        
        $subjectDropdown.addClass("open");
        $classDropdown.removeClass("open");
    });
    
    $subjectDropdown.on("click", ".dropdown-item", function (e) {
        e.stopPropagation();
        const rawSubject = $(this).data("value");
        currentSubject = rawSubject;

        const filename = subjects[currentClass][currentSubject];

        $("#next-question").off("click").click(() => {
            $("#result").text("");
            $("#explanation").text("");
            $("#explanation-box").hide();
            loadQuestion('truefalse', filename);
        });

        $subjectTitle.text($(this).text()).addClass("selected");
        $(".custom-dropdown").removeClass("open");

        if (currentClass && currentSubject) {
            loadQuestion('truefalse', filename);
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