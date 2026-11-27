//Header and Welcome
async function loadName(){
    const res = await fetch('/api/me')
    if (!res.ok) return
    const user = await res.json()
    const name = document.getElementById('welcome-name') // sets name to welcome name element
    name.textContent = user.username + '!'

}

//Session Log (first written)
async function loadSessions(){
    const res = await fetch('/api/sessions') //session data in res
    if (!res.ok) return // check if server replies, if not dont load sessions

    const sessions = await res.json() //session data in sessions as list
    const list = document.getElementById('session-list') // list = session-list
    list.innerHTML = '' //sets list to empty

    for(const s of sessions){ // of gives items, in gives index
        const li = document.createElement('li')
        li.textContent = s.date + ' - ' + s.exercise_count + ' exercises'
        list.appendChild(li)
    }
}

//calling all functions (dashboard html loads dashboard.js)
loadName()