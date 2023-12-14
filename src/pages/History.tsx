import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import IEvent from '../API/models/ins'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'
import FormCalendar from '../components/FormCalendar'
import isInclude from '../utils/isInclude'
import sortDate from '../utils/sortDate'

const History:FC = ()=> {
    const navigate = useNavigate()

    const [events, setEvents] = useState<IEvent[]>([])

    const [eventName, setEventName] = useState<string>('')

    const [rangeDate, setRangeDate] = useState<IRangeDate>({'from': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}, 'to': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}})

    const [currentDates, setCurrentDates] = useState<IDate[]>([])

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
    
    async function fetchGetUser (token: string) {
        const response = await PostService.getUser(token)
        if (response.userName) {
          console.log(response.userName)
        } else {
          navigate('/login')
        }
      }

    async function fetchGetEvents (token: string) {
        const response = await PostService.getEvents(token)
        if (response) {
          setEvents(response)
          if (response[0]){
            setEventName(response[0].name)
          }
        }
      }

    const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
      e.currentTarget.click()
      e.preventDefault()

      let currentEventDates: Array<IDate> = []
      setCurrentDates([])

      for (let i=0; i < events.length; i++){
        if(events[i].name==eventName){
          let eventDates = events[i].time
          currentEventDates = eventDates.filter((checkDate)=> isInclude(rangeDate.from, rangeDate.to, checkDate))
          break
      }}
      
      if (currentEventDates.length !== 0){
        currentEventDates = sortDate(currentEventDates)
        setCurrentDates(currentEventDates)
      }
    }

    const onClickMain = (e: React.MouseEvent<HTMLElement>)=>{
      e.preventDefault()
      navigate('/')
    }

    
    return(
        <div>
          <div className='topHistory'>
          <h1 className="headerHistory">История</h1>
          <a className="linkMain"onClick={onClickMain}>Главная</a>
          </div>
          <FormCalendar onSubmit={onSubmit}  onChangeEvent={setEventName} setDate={setRangeDate} eventName={eventName} type={true} events={events}/>
          {currentDates.length !== 0 ?
            <div>
            <div className='historyEventHeader'>Событие - <strong>{eventName}</strong> ||||||||||||| количество - <strong>{currentDates.length}</strong> </div>
            <ul className='dates'>
            {currentDates.map( (date, i)=> <li className='dateCell' key={i}>{date.year}.{date.month}.{date.day}  {date.hour}:{date.minute}</li>)}
            </ul>
            </div>
            :
            <div>за указанный период события - <strong>{eventName}</strong> - вы не делали</div>
          }
        </div>
    )
}
export default History