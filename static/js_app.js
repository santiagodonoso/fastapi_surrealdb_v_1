// ##############################
async function create_user(){
  const form = event.target
  console.log(form)
  const conn = await fetch('/users', {
    method : "POST",
    body : new FormData(form)
  })
  const data = await conn.json()
  if(!conn.ok){
    console.log('Error in the system')
    console.log(data)
    return
  }
  user = data.result[0]
  console.log(data)
  document.querySelector("#users").insertAdjacentHTML('afterbegin', `
    <form class="user" onsubmit="return false">
      <div class="user_id">
        ${user.id}
      </div>
      <div class="user_name">
      ${user.user_name}
      </div>
      <div class="user_email">
      ${user.user_email}
      </div>
      <button class="user_delete" onclick="delete_user('${user.id}')">
        🗑️
      </button>
    </form>  
  `)
}

// ##############################
async function delete_user(user_id){
  try{
    console.log("Deleting user...", user_id)
    form = event.target.form
    const conn = await fetch(`/users/${user_id}`, {
      method : "DELETE"
    })
    form.remove()
  }catch(error ){
    console.log(error)
  }
}