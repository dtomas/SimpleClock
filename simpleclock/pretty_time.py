import time

day_name = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'), _('Friday'),
        _('Saturday'), _('Sunday')]

month_name = ['', _('January'), _('February'), _('March'), _('April'),
          _('May'), _('June'), _('July'), _('August'),
          _('September'), _('October'), _('November'), _('December')]

about_message = [_('nearly'), _('nearly'), _('about'), _('just gone'), _('just gone')]

section_name = ['', _('five past '), _('ten past '), _('a quarter past '),
            _('twenty past '), _('twenty-five past '), _('half past '),
        _('twenty-five to '), _('twenty to '), _('a quarter to '),
        _('ten to '), _('five to ')]

# Necessary for translation. Some languages use the next hour for the 
# description of some sections. This is the number of the first section for
# which the next hour is used.
sections_separator = _('7')

number = [None, _('one'), _('two'), _('three'), _('four'), _('five'), _('six'),
       _('seven'), _('eight'), _('nine'), _('ten'), _('eleven')]

def hour_name(hour):
    assert hour >= 0 and hour < 24

    if hour == 0:
        return _("midnight")
    elif hour == 12:
        return _("noon")
    return number[hour % 12]

def th(n):
    "Cardinal integer to ordinal string."
    if n > 3 and n < 20:
        return _("%dth") % n

    d = n % 10
    if d == 1:
        return _("%dst") % n
    elif d == 2:
        return _("%dnd") % n
    elif d == 3:
        return _("%drd") % n
    else:
        return _("%dth") % n

def rough_time(time_in_seconds, show_time = True, show_date = True):
    "Convert a time (as returned by time()) to a string."
    assert show_time or show_date
    t = time.localtime(time_in_seconds + 150)
    year, month, day, hour, minute, second,    weekday, julian, dst = t

    off = about_message[minute % 5]

    if minute / 5 >= int(sections_separator):
        hour = (hour + 1) % 24

    if minute / 5 == 0 and hour != 0 and hour != 12:
        o_clock = _(" o'clock")
    else:
        o_clock = ""

    if show_time and not show_date:
        return _("It's %s %s%s%s.") % (about_message[minute % 5],
                                           section_name[minute / 5],
                                           hour_name(hour), o_clock)
    if show_date and not show_time:
        return _("It's %s, the %s %s %s.") % (day_name[weekday], 
                                                th(day), 
                                                month_name[month],
                                                year)
    if show_time and show_date:
        return _("It's %s %s%s%s on %s, the %s %s %s.") \
                                        % (about_message[minute % 5],
                                              section_name[minute / 5],
                                               hour_name(hour), o_clock,
                                               day_name[weekday], 
                                            th(day), 
                                            month_name[month],
                                            year)

def str_time(hour = None, min = None):
    if hour == None:
        t = time.localtime(time.time())
        year, month, day, hour, min, second, weekday, julian, dst = t

    h = hour % 12
    if h == 0:
        h = 12
    if hour < 12:
        am = _('am')
    else:
        am = _('pm')
    return _('%s:%02d %s') % (h, min, am)
