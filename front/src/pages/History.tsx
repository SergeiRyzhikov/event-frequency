import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'

const History:FC = ()=> {
    useEffect(() => {
        console.log('useEffect')
        // if (localStorage.getItem('token')){
        //   fetchGetUser(String(localStorage.getItem('token')))
        //   fetchGetEvents(String(localStorage.getItem('token')))
        // }
        // else{
        //   navigate('/login')
        // }
        
    }, [localStorage])
    return(
        <div></div>
    )
}
export default History