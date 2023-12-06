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
        <img src="photo.jpg"  alt="" />
    </div>
  )
}

export default Main
