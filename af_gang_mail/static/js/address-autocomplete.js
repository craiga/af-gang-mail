// Address Autocomplete
// https://developers.google.com/maps/documentation/javascript/reference/places-widget

document.addEventListener("DOMContentLoaded", function (event) {
  const addressSearchField = document.getElementById("id_street_address");
  if (addressSearchField) {
    let autocomplete = new google.maps.places.Autocomplete(addressSearchField, {
      fields: ["address_components"],
    });

    const countrySelect = document.getElementById("id_address_country");
    const country = countrySelect[countrySelect.selectedIndex].value;
    if (country) {
      autocomplete.setComponentRestrictions({ country: country });
    }

    countrySelect.addEventListener("change", (event) => {
      const country = countrySelect[countrySelect.selectedIndex].value;
      if (country) {
        autocomplete.setComponentRestrictions({ country: country });
      }
    });

    autocomplete.addListener("place_changed", function () {
      const place = autocomplete.getPlace();
      const address = {};

      for (let addressComponent of place["address_components"]) {
        const types = addressComponent["types"];

        if (types.includes("street_number")) {
          if (!("street_address" in address)) {
            address["street_address"] = "";
          }
          address["street_address"] =
            addressComponent["long_name"] + " " + address["street_address"];
        }

        if (types.includes("route")) {
          if (!("street_address" in address)) {
            address["street_address"] = "";
          }
          address["street_address"] =
            address["street_address"] + addressComponent["long_name"];
        }

        if (types.includes("locality") || types.includes("postal_town")) {
          address["address_city"] = addressComponent["long_name"];
        }

        if (types.includes("administrative_area_level_1")) {
          address["address_state"] = addressComponent["long_name"];
        }

        if (types.includes("postal_code")) {
          address["address_postcode"] = addressComponent["long_name"];
        }

        if (types.includes("country")) {
          address["address_country"] = addressComponent["short_name"];
        }
      }

      for (let fieldName in address) {
        for (const field of document.getElementsByName(fieldName)) {
          field.value = address[fieldName];
        }
      }
    });
  }
});
