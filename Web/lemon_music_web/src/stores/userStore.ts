import { ref } from 'vue'
import { defineStore } from 'pinia'


export class User {
    username = ''
    userId = ''
    token = ''

    constructor(token, userId, username) {        
        this.token = token
        this.username = username;
        this.userId = userId;
    }
}

export const useUserStore = defineStore('user', () => {
    
    var localUser = new User('', '', '')

    var localUserString = sessionStorage.getItem('user')    
    if (localUserString == null) {
        localUserString = localStorage.getItem('user');
    }
    if (localUserString != null) {
        var localUserObj = JSON.parse(localUserString)
        localUser = new User(localUserObj['token'], localUserObj['userId'], localUserObj['username']);
    } 
    
    const user = ref(localUser)    

    function refreshUser(user) {
        let uservalue = JSON.stringify(user)
        sessionStorage.setItem('user', uservalue);
        localStorage.setItem('user', uservalue);
    }

    function cleanUser() {
        sessionStorage.removeItem('user')
        localStorage.removeItem('user')
    }

    return { user, refreshUser, cleanUser }
})
