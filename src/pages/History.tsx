import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import IEvent from '../API/models/ins'
import { DtPicker } from 'react-calendar-datetime-picker'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'
// import {} from '../types/types'
import FormCalendar from '../components/FormCalendar'

const History:FC = ()=> {
    const navigate = useNavigate()

    const [userName, setUserName] = useState<string>('')

    const [events, setEvents] = useState<IEvent[]>([])

    const [eventName, setEventName] = useState<string>('')

    const [date, setDate] = useState<IDate>({'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11})

    const [rangeDate, setRangeDate] = useState<IRangeDate>({'from': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}, 'to': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}})

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

    const onChangeEvent =(e: React.ChangeEvent<HTMLInputElement>)=>{
      setEventName(e.target.value.toLowerCase())
    }

    const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
      e.currentTarget.click()
      e.preventDefault()
      
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
        <div>
          <h1 className="headerHistory">История</h1>
          <FormCalendar onSubmit={onSubmit}  onChangeEvent={onChangeEvent} setDate={setRangeDate} eventName={eventName} type={true}/>
        </div>
    )
}
export default History