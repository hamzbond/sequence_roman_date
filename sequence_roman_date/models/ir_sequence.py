# -*- coding: utf-8 -*-

from datetime import datetime

import pytz

from odoo import api, models, _
from odoo.exceptions import UserError


class RomanNumeralService(object):

    MONTH_ROMAN_MAP = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
    }

    YEAR_ROMAN_VALUES = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    @classmethod
    def month_to_roman(cls, month_number):
        try:
            month_int = int(month_number)
            if 1 <= month_int <= 12:
                return cls.MONTH_ROMAN_MAP[month_int]
            return str(month_number)
        except (ValueError, TypeError):
            return str(month_number)

    @classmethod
    def year_to_roman(cls, year_number):
        try:
            year_int = int(year_number)
            if not 1 <= year_int <= 4999:
                return str(year_number)

            result = ''
            for value, numeral in cls.YEAR_ROMAN_VALUES:
                count = year_int // value
                if count:
                    result += numeral * count
                    year_int -= value * count
            return result
        except (ValueError, TypeError):
            return str(year_number)


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.multi
    def _get_prefix_suffix(self):
        uses_custom_legend = any(
            '%(month_roman)s' in (rec.prefix or '') or '%(month_roman)s' in (rec.suffix or '') or
            '%(year_roman)s' in (rec.prefix or '') or '%(year_roman)s' in (rec.suffix or '')
            for rec in self
        )
        if not uses_custom_legend:
            return super(IrSequence, self)._get_prefix_suffix()

        now = range_date = effective_date = datetime.now(
            pytz.timezone(self._context.get('tz') or 'UTC')
        )
        if self._context.get('ir_sequence_date'):
            effective_date = datetime.strptime(self._context.get('ir_sequence_date'), '%Y-%m-%d')
        if self._context.get('ir_sequence_date_range'):
            range_date = datetime.strptime(self._context.get('ir_sequence_date_range'), '%Y-%m-%d')

        sequences = {
            'year': '%Y', 'month': '%m', 'day': '%d', 'y': '%y', 'doy': '%j', 'woy': '%W',
            'weekday': '%w', 'h24': '%H', 'h12': '%I', 'min': '%M', 'sec': '%S'
        }
        interpolation_dict = {}
        for key, fmt in sequences.items():
            interpolation_dict[key] = effective_date.strftime(fmt)
            interpolation_dict['range_' + key] = range_date.strftime(fmt)
            interpolation_dict['current_' + key] = now.strftime(fmt)

        interpolation_dict['month_roman'] = RomanNumeralService.month_to_roman(interpolation_dict['month'])
        interpolation_dict['year_roman'] = RomanNumeralService.year_to_roman(interpolation_dict['year'])

        def _interpolate(value, data):
            return (value % data) if value else ''

        record = self[0]
        try:
            prefix = _interpolate(record.prefix, interpolation_dict)
            suffix = _interpolate(record.suffix, interpolation_dict)
        except ValueError:
            raise UserError(_('Invalid prefix or suffix for sequence "%s"') % (record.name,))

        return prefix, suffix
