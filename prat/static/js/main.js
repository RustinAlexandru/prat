
function postCompleteTask(data) {
    showOverlay();

    var modal = $(".modal-task-completed");
    var h4 = modal.find('h4');
    h4.text(data.task);

    var details = modal.find('.details');
    details.empty();
    details.append($("<p></p>").text("+" + data.points + " Points"));
    details.append($("<p></p>").text("+" + data.experience + " Experience"));
    modal.slideDown();
}

function hideModal(className) {
    var modal = $("." + className);
    modal.slideUp();
    hideOverlay();
}

function showOverlay() {
    var overlay = $(".overlay");
    if (overlay.hasClass('active')) {
        return;
    }

    overlay.toggleClass('active');
}

function hideOverlay() {
    var overlay = $(".overlay");
    if (!overlay.hasClass('active')) {
        return;
    }

    overlay.toggleClass('active');
    window.location.reload();
}