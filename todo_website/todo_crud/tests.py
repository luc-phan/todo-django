from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command


from .models import Todo

# Create your tests here.


class  TodoIndexViewTests(TestCase):
    def test_nothing_todo(self):
        """
        If no TODO exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing TODO.")
        self.assertEqual(len(response.context['formset']), 0)

    def test_demo_todo(self):
        """
        The index page may display all TODOs.
        """
        call_command('loaddata', 'demo', verbosity=0)
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['formset']), 3)

        todos = Todo.objects.all()
        self.assertQuerysetEqual(
            set(form.instance for form in response.context['formset']),
            set(todos),
        )

    def test_reverse_state(self):
        """
        The index page can update all TODOs' states.
        """
        call_command('loaddata', 'demo', verbosity=0)
        response = self.client.get(reverse('index'))

        data = dict()
        formset = response.context['formset']

        # global information, some additional fields may go there
        data['csrf_token'] = response.context['csrf_token']

        # management form information, needed because of the formset
        management_form = formset.management_form

        for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
            data[f'{management_form.prefix}-{i}'] = management_form[i].value()

        for i in range(formset.total_form_count()):
            # get form index 'i'
            current_form = formset.forms[i]

            # retrieve all the fields
            for field_name in current_form.fields:
                value = current_form[field_name].value()
                if field_name == 'done':
                    data[f'{current_form.prefix}-{field_name}'] = not value  # reverse state
                else:
                    data[f'{current_form.prefix}-{field_name}'] = value if value is not None else ''

        response = self.client.post(reverse('index'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        states = {form.instance.id:form.instance.done for form in response.context['formset']}
        self.assertEqual(states, {1:True, 2:False, 3:True})


class TodoDetailViewTests(TestCase):
    def test_todo_not_found(self):
        """
        The detail view of a non-existing todo returns a 404 not found.
        """
        url = reverse('detail', args=(123,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_a_todo(self):
        """
        The detail view of an existing todo displays the todo's title and description.
        """
        call_command('loaddata', 'demo', verbosity=0)
        url = reverse('detail', args=(1,))
        response = self.client.get(url)
        self.assertContains(response, "One-two, one-two, this is a test")
        self.assertContains(response, "Lorem ipsum dolor sit amet")


class TodoCreateViewTests(TestCase):
    def test_new_todo_form(self):
        """
        The create view displays a TODO form.
        """
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Title")
        self.assertContains(response, "Description")

    def test_new_todo_creation(self):
        """
        Posting the form creates a TODO.
        """
        response = self.client.get(reverse('new'))
        response = self.client.post(
            reverse('new'),
            {
                'title': "New title",
                'description': "New description"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
