document.addEventListener('click', (e) => {
    const isDropDownButton = e.target.matches('[data-dropdown-button]')
    if(!isDropDownButton && e.target.closest('[data-dropdown]') != null) return;

    let currentDropdown
    if (isDropDownButton){
        currentDropdown = e.target.closest('[data-dropdown]')
        currentDropdown.classList.toggle('active')
    }
    document.querySelectorAll('[data-dropdown].active').forEach( dropdown => {
        if(dropdown === currentDropdown) return;
        dropdown.classList.remove('active')
    })
})

function scrollHeader() {
  const nav = document.getElementById("nav")
  if (this.scrollY >= 150) nav.classList.add("scroll-header")
  else nav.classList.remove("scroll-header")
}

window.addEventListener("scroll", scrollHeader)

// modal
const modalBtns = document.querySelectorAll('.modal-btn')
modalBtns.forEach((btn) => {
  console.log(btn)
  btn.addEventListener('click', () => {
    closeFlashMessage(btn)
  })
})

function closeFlashMessage(btn){
  let modal = btn.closest('.modal')
  console.log(modal)
  modal.classList.add('inactive')
}

// Like fn
function like(postId) {
  const likesCount = document.getElementById(`likes-count-${postId}`)
  const likesButton = document.getElementById(`like-button-${postId}`)

  fetch(`/posts/like-post/${postId}`, {method: "POST"})
    .then((res) => res.json())
    .then((data) => {
      console.log(data)
      likesCount.innerText = data["likes"]
    })
    .catch((e) => alert("couldn't like post"))
}

