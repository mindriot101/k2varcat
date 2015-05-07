$(function() {
    $('#summary').DataTable({
        processing: false,
        pageLength: 25,
        ajax: {
            url: "https://spreadsheets.google.com/feeds/list/11Y0WIAQwOVJi-2mP9oVEzHg1EActd6sNxaYfwZT1SB4/od6/public/values?alt=json",
            dataSrc: "feed.entry",
        },
        columns: [
            { "data": "gsx$epicid.$t" },
            { "data": "gsx$type.$t" },
            { "data": "gsx$range.$t" },
            { "data": "gsx$period.$t" },
            { "data": "gsx$amplitude.$t" },
            { "data": "gsx$proposal.$t" },
        ],
    });

    /* Add click handler to each row to open detail page */
    $('#summary tbody').on('click', 'tr', function() {
        var epic_id = $('td', this).eq(0).text();
        var url = "/objects/" + epic_id + ".html";
        window.open(url, epic_id, "");
        return false;
    });
});
