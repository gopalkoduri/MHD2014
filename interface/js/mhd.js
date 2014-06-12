var current_elements = {images:[], sounds:[]}
make_embed_sound = function(sound) {
    return "<div class=\"sound\" " + "id=\"" + sound.id + "\">" +
           "<div class=\"click\" onclick=\"click_element(" +sound.id + ")\"></div>" +
           "<iframe frameborder=\"0\" scrolling=\"no\" src=\"" +
           sound.embed_url + "\" width=\"481\" height=\"86\"></iframe></div>";
};

make_embed_image = function(image) {
    return "<div class=\"image\" " + " id=\"" +image.id + "\">" +
           "<div class=\"click\" onclick=\"click_element(" + image.id + ")\"></div>" +
           "<iframe src=\"" + image.embed_url+ "\" height=\"424\" width=\"500" +
           "frameborder=\"0\" >";
}

click_element = function(event) {
    var target = event.target;
    console.log(target);
    var current_ids = {images: [], sounds: []}

    $.each(current_elements.images, function(index, image) {
        current_ids.images.push(image.id);
    });

    $.each(current_elements.sounds, function(index, sound) {
        current_ids.sounds.push(sound.id);
    });

    $.ajax({
        url:"/getmore/" + target,
        type: "GET",
        data: current_ids,
        success: build_gui,
        fail: function() { console.log("error getting moar sounds and images") }
    });
}

build_gui = function(data) {
    current_elements = data;
    $("#photo_container").empty();
    $.each(data.images, function(index, element) {
        $("#photo_container").append(make_embed_image(element));
        current_ids.images
    });
    $("#sound_container").empty();
    $.each(data.sounds, function(index, element) {
        $("#sound_container").append(make_embed_sound(element));
    });
};

    
