import React, { ChangeEventHandler, FC, FormEventHandler } from 'react'
import { DtPicker } from 'react-calendar-datetime-picker'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'
import IEvent from '../API/models/ins'

interface IForm {
    eventName: string
    onChangeEvent: ChangeEventHandler<HTMLInputElement> | any
    onSubmit: FormEventHandler<HTMLFormElement>
    setDate: React.Dispatch<React.SetStateAction<IDate>> | React.Dispatch<React.SetStateAction<IRangeDate>>
    type: boolean
    events: IEvent[]
}

const FormCalendar:FC<IForm> = ({onSubmit, eventName, onChangeEvent, setDate, type, events}) => {
  return (
    <form action="" onSubmit={onSubmit}>  
          {type ?
            <div>
            <select required onChange={e => {onChangeEvent(e.target.value)}}>
            <option disabled >Выберите ваше событие</option>
            {events.map( (event, i) => <option key={i} >{event.name}</option> )}
            </select>
            <DtPicker  
            onChange={setDate}
            type='range'
            local='en'
            inputClass='customInputCalendar'
            withTime
            isRequired
            showTimeInput
            placeholder='Выберите период времени'
            showWeekend/>
            </div>
            :
            <div>
            <input type="text" placeholder='введите событие'className='inputMain' value={eventName} onChange={onChangeEvent}/> 
            <DtPicker  
            onChange={setDate}
            type='single'
            local='en'
            withTime
            isRequired
            inputClass='customInputCalendar'
            placeholder='Выберите дату события'
            showTimeInput
            showWeekend/>
            </div>
          }
          <button type='submit' className='send'>отправить</button>
        </form>
  )
}

export default FormCalendar