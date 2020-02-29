document.addEventListener('DOMContentLoaded', () =>{

  if(document.querySelector('#settings-btn')){
    document.querySelector('#settings-btn').onclick = () =>{

        var x = document.querySelector('.my-card');
        if (x.style.display === "none") {
          x.style.display = "flex";
        } else {
          x.style.display = "none";
        }


    }
  }

    var if_present = document.querySelector(".profile-edit-modal");
    if(if_present){

    document.querySelector('#appear_pic').onclick = () =>{
      document.querySelector('#bio-form').style.display = "none";
      document.querySelector('.profile-edit-modal').style.display = "flex"; 
      document.querySelector('#pic-form').style.display = "flex";
    }

    document.querySelector('#appear_bio').onclick = () =>{
      document.querySelector('#pic-form').style.display = "none";
      document.querySelector('.profile-edit-modal').style.display = "flex";     
      document.querySelector('#bio-form').style.display = "flex";
    }
    
    var pic_form = document.querySelector('#pic-form');
    var bio_form = document.querySelector('#bio-form');

    document.querySelector('#cancel').onclick = () =>{
      document.querySelector('.profile-edit-modal').style.display = "none";

      if (pic_form.style.display === "flex") {
        pic_form.style.display = "none";
      } else if(bio_form.style.display === "none") {
        bio_form.style.display = "none";
      }
    }

  }

    if(document.querySelector('#followers-btn') && document.querySelector('#following-btn')){
    document.querySelector('#followers-btn').onclick = () =>{
      if (document.querySelector('#follow-child-right').style.display !== "none"){

      document.querySelector('#follow-child-right').style.display = "none";
    }
      document.querySelector('#follow-child-left').style.display = "block";
      document.querySelector('#exampleModalLongTitle').innerHTML = "Followers";
    }

    document.querySelector('#following-btn').onclick = () =>{

      if (document.querySelector('#follow-child-left').style.display !== "none"){
        
        document.querySelector('#follow-child-left').style.display = "none";
      }

      document.querySelector('#follow-child-right').style.display = "block";
      document.querySelector('#exampleModalLongTitle').innerHTML = "Following";
    }
  }

})