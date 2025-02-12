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
    const $questionText = $("#question");
    const $answerBox = $("#answer-box");
    const $explanationBox = $("#explanation-box");
    const $resultText = $("#result");
    const $explanationText = $("#explanation");
    const $optionsContainer = $("#options-container");

    $("#submit-answer").click(submitAnswer);
    $("#show-explanation").click(showExplanation);
    $("#next-question").click(loadNextQuestion);

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

    $questionText.text("Please select a class and subject.");
    $answerBox.hide();
    $explanationBox.hide();

    $classDropdown.on("click", ".dropdown-item", function (e) {
        e.stopPropagation();
        currentClass = $(this).data("value");
        $classTitle.text($(this).text()).addClass("selected");

        currentSubject = null;
        $subjectTitle.text("Select Subject").removeClass("selected");
        $questionText.text("Please select a class and subject.");
        $answerBox.hide();
        $explanationBox.hide();

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

        loadQuestion('mcq', filename);

        $subjectTitle.text($(this).text()).addClass("selected");
        $(".custom-dropdown").removeClass("open");
    });

    function loadQuestion(type, filename) {
        $questionText.text("Loading question...");
        $answerBox.hide();
        $explanationBox.hide();
        $resultText.text("");
        $explanationText.text("");

        $.get(`/ask_question?type=${encodeURIComponent(type)}&file=${encodeURIComponent(filename)}`)
            .done(data => {
                if (data.question && data.options && data.correct_option) {
                    displayQuestion(data);
                } else {
                    $questionText.text("Failed to load question. Try again.");
                }
            })
            .fail(() => {
                $questionText.text("Error loading question. Please try again.");
            });
    }

    function displayQuestion(data) {
        $questionText.text(data.question).data('correct-answer', data.correct_option);

        $optionsContainer.empty();

        data.options.forEach((option, index) => {
            const optionNumber = index + 1;
            const optionHtml = `
                <div class="option">
                    <input type="radio" name="mcq" id="option${optionNumber}" value="${option}">
                    <label for="option${optionNumber}" class="option-label">
                        <span class="option-text">${option}</span>
                    </label>
                </div>
            `;
            $optionsContainer.append(optionHtml);
        });

        $answerBox.show();
        $explanationBox.show();
        $("#submit-answer").prop('disabled', false);
        $('input[name="mcq"]').prop('checked', false);
    }

    function submitAnswer() {
        const selectedOption = $('input[name="mcq"]:checked');
        if (!selectedOption.length) return;

        totalCount++;
        const userAnswer = selectedOption.val();
        const correctAnswer = $questionText.data('correct-answer');
        const optionElement = selectedOption.closest('.option');

        $("#submit-answer").prop('disabled', true);
        // $('input[name="mcq"]').prop('disabled', true);

        if (userAnswer === correctAnswer) {
            correctCount++;
            optionElement.addClass('correct-answer');
            $resultText.text("Correct!")
        } else {
            wrongCount++;
            optionElement.addClass('wrong-answer');
            $(`input[value="${correctAnswer}"]`).closest('.option')
                .addClass('correct-answer')
            $resultText.text("Incorrect")
        }

        updateCounters();
        showExplanation();
    }

    function showExplanation() {
        $.post("/show_explanation", function (data) {
            if (data.explanation) {
                $explanationText.text(data.explanation);
            }
        });
    }

    function loadNextQuestion() {
        if (currentClass && currentSubject) {
            const filename = subjects[currentClass][currentSubject];
            loadQuestion('mcq', filename);
        }
    }

    function updateCounters() {
        $("#correct-count").text(correctCount);
        $("#wrong-count").text(wrongCount);
        $("#total-count").text(totalCount);
    }
});