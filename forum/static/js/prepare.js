
$(document).ready(function () {
    $("input[name=someRadioGroup]:radio").change(function () {
        if ($("#r1").attr("checked")) {
            alert("r1 selected");
        }
        else {
            alert("r2 or r3 selected");
            document.getElementById("content2").innerHTML = "clicked";

        }
        $('#log').val($('#log').val()+ $(this).val() + '|');

    })
});
