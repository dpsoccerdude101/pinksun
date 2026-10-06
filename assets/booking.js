/* PinkSun — booking handoff wiring.
 *
 * Every reservation call to action on the site carries data-booking (optionally
 * with a product path). This file is the ONLY place the platform URL lives.
 *
 * To go live: set BOOKING_URL to the reservation portal, e.g.
 *   const BOOKING_URL = "https://app.courtreserve.com/Online/Portal/Index/12345";
 * CourtReserve is the default assumption because every dedicated club in the
 * Rochester market uses it and it supports per-product deep links.
 *
 * While BOOKING_URL is empty the funnel stays honest: the links point at the
 * on-page notice instead of inventing a third-party URL that might belong to
 * somebody else's club.
 */
(function () {
  var BOOKING_URL = ""; // <-- set this to wire the whole funnel to a live platform

  var links = document.querySelectorAll("[data-booking]");
  var note = document.getElementById("booking-note");

  links.forEach(function (a) {
    if (BOOKING_URL) {
      var path = a.getAttribute("data-booking-path") || "";
      a.href = BOOKING_URL + path;
      a.target = "_blank";
      a.rel = "noopener";
      a.removeAttribute("data-booking-pending");
    } else {
      a.setAttribute("href", "#booking-note");
      a.setAttribute("data-booking-pending", "true");
      a.addEventListener("click", function () {
        if (!note) return;
        note.hidden = false;
        note.focus({ preventScroll: false });
      });
    }
  });

  if (note) {
    var back = note.querySelector("[data-booking-close]");
    if (back) back.addEventListener("click", function () { note.hidden = true; });
  }
})();
