import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'

const History:FC = ()=> {
    const navigate = useNavigate()

    const [userName, setUserName] = useState()

    const [events, setEvents] = useState()

    async function fetchGetUser (token: string) {
        console.log('jjjj')
        const response = await PostService.getUser(token)
        console.log('kk')
        if (response.userName) {
          setUserName(response.userName)
          console.log(response.userName)
        } else {
          navigate('/login')
          console.log('34')
        }
      }

    async function fetchGetEvents (token: string) {
        const response = await PostService.getEvents(token)
        console.log(response)
        if (response) {
          setEvents(response)
          console.log(response)
        } else {
          console.log('34')
        }
      }
    
    useEffect(() => {
        console.log('useEffect')
        if (localStorage.getItem('token')){
          fetchGetUser(String(localStorage.getItem('token')))
          fetchGetEvents(String(localStorage.getItem('token')))
        }
        else{
          navigate('/login')
        }
        
    }, [localStorage])
    return(
        <div>История

        </div>
    )
}
export default History