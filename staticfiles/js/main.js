$(document).ready(function () {
    $('.inline').on('click', function () {
        var image = $(this).attr('src');
        alert(image);
        $('#myModal').on('show.bs.modal', function () {
            $(".showimage").attr("src", image);
        });
    });
});
