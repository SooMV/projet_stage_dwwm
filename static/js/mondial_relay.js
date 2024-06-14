// Init the widget on ready state
document.addEventListener('DOMContentLoaded', (function() {
  $("#Zone_Widget").MR_ParcelShopPicker({
    Target: "#Target_Widget",
    
    Brand: "BDTEST  ",
    // Default Country (2 letters) used for search at loading
    Country: "FR",
    // Default postal Code used for search at loading
    PostCode: "75001",
    // Delivery mode (Standard [24R], XL [24L], XXL [24X], Drive [DRI])
    ColLivMod: "24R",
    // Number of parcelshops requested (must be less than 20)
    NbResults: "7",
    TargetDisplay: "#TargetDisplay_Widget",
    TargetDisplayInfoPR: "#TargetDisplayInfoPR_Widget",
  
    
    Responsive: true,
        // Show the results on Leaflet map usng OpenStreetMap. 
    ShowResultsOnMap: true,
    EnableGeolocalisatedSearch : true,
    OnParcelShopSelected:
    function(data) {
      $("#cb_ID").html(data.ID);
      $("#cb_Nom").html(data.Nom);
      $("#cb_Adresse").html(data.Adresse1 + ' ' + data.Adresse2);
      $("#cb_CP").html(data.CP);
      $("#cb_Ville").html(data.Ville);
      $("#cb_Pays").html(data.Pays);
      }
  });

}));
