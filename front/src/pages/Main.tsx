import React, { FC, useEffect, useRef, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import { DtPicker} from 'react-calendar-datetime-picker'
import 'react-calendar-datetime-picker/dist/style.css'

import IEvent from '../API/models/ins'

import IDate from '../types/types'
import Event from '../components/Event'

const Main:FC = () =>{
  const [userName, setUserName] = useState<string>('')

  const [date, setDate] = useState<IDate>({'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11})

  const [eventName, setEventName] = useState<string>('')

  const [events, setEvents] = useState<Array<IEvent>>([])

  const navigate = useNavigate()

  const calendarRef = useRef<HTMLDivElement>() as React.MutableRefObject<HTMLDivElement>


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

  async function fetchCreateEvent (token: string, name: string, time:IDate) {
    console.log(token, name, time)
    const response = await PostService.createEvent(token, name, time)
    console.log('kk')
    if (response) {
      fetchGetEvents(String(localStorage.getItem('token')))
    } else {
      console.log('34')
    }
  }

  async function fetchDeleteEvent (token: string, name: string, time:IDate) {
    const response = await PostService.deleteEvent(token, name, time)
    console.log(response)
    if (response) {
      fetchGetEvents(String(localStorage.getItem('token')))
    } else {
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

  const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
    e.currentTarget.click()
    e.preventDefault()
    console.log(eventName, date)
    fetchCreateEvent(String(localStorage.getItem('token')), eventName, date)
  }

  const onchangeEvent =(e: React.ChangeEvent<HTMLInputElement>)=>{
    setEventName(e.target.value.toLowerCase())
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

  return (
    <div>
      <div className='top'>
      
        <div>
        <div>Вечер в хату {userName}</div>
        <h1>Как часто?</h1>

        </div>
        <a>ИСТОРИЯ</a>
        
        </div>
        <form action="" onSubmit={onSubmit}>
          <input type="text" placeholder='введите событие' value={eventName} onChange={onchangeEvent}/> 
          <div className="calendar" ref={calendarRef} >
          <DtPicker  
          onChange={setDate}
          type='single'
          local='en'
          withTime
          isRequired
          showTimeInput
          showWeekend/>
          </div>
          <button type='submit' className='send'>отправить</button>
        </form>
        {events &&
          <div>
            {events.map( (event) => <Event name={event.name} time={event.time} fetchDeleteEvent={fetchDeleteEvent}/> )}
            </div>
        }
        <img src="data:image/jpeg;base64,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" alt="" />
    </div>
  )
}

export default Main
