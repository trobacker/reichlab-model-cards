"""
Generate spider/radar plots for model performance rankings across multiple metrics.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib.patches as mpatches


def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.
    """
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
            return lines

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def generate_spider_plot(model_name, metrics_data, output_path, total_models=None):
    """
    Generate a spider plot showing model rankings across evaluation metrics.

    Parameters
    ----------
    model_name : str
        Name of the model (e.g., "UMass-flusion")
    metrics_data : dict
        Dictionary with metric names as keys and ranking info as values.
        Each value should be a dict with 'rank' and optionally 'total_models'.
        Example: {
            'WIS 0-week': {'rank': 3, 'total_models': 20},
            'WIS 1-week': {'rank': 5, 'total_models': 20},
            ...
        }
    output_path : str
        Path to save the spider plot image
    total_models : int, optional
        Total number of models (if not specified per metric)

    Returns
    -------
    str
        Path to the generated plot
    """

    # Extract metric names and ranks
    metrics = list(metrics_data.keys())
    ranks = []

    for metric in metrics:
        rank = metrics_data[metric]['rank']
        n_models = metrics_data[metric].get('total_models', total_models)
        if n_models is None:
            raise ValueError(f"Total models not specified for {metric}")

        # Convert rank to inverted percentile (1st place = 100%, last place = 0%)
        # This makes better models appear larger on the plot
        percentile = 100 * (n_models - rank + 1) / n_models
        ranks.append(percentile)

    # Number of variables
    N = len(metrics)

    # Create the radar plot
    theta = radar_factory(N, frame='polygon')

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    # Plot data
    ax.plot(theta, ranks, 'o-', linewidth=2, color='#2E86AB', markersize=8)
    ax.fill(theta, ranks, alpha=0.25, color='#2E86AB')

    # Set axis labels
    ax.set_varlabels(metrics)

    # Set y-axis range (percentile)
    ax.set_ylim(0, 100)

    # Add gridlines at 25%, 50%, 75%, 100%
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=10, color='gray')

    # Add title
    plt.title(f'{model_name}\nPerformance Rankings Across Metrics',
              position=(0.5, 1.1), ha='center', fontsize=14, fontweight='bold')

    # Add legend explaining the percentile scale
    legend_text = "100% = Rank 1st | 0% = Last Place"
    plt.figtext(0.5, 0.02, legend_text, ha='center', fontsize=10,
                style='italic', color='gray')

    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    return output_path


def generate_sample_spider_plot():
    """Generate a sample spider plot with mock data for UMass-flusion."""

    # Sample data - UMass-flusion rankings across different metrics
    metrics_data = {
        'WIS\n0-week': {'rank': 3, 'total_models': 20},
        'WIS\n1-week': {'rank': 5, 'total_models': 20},
        'WIS\n2-week': {'rank': 4, 'total_models': 20},
        'WIS\n3-week': {'rank': 6, 'total_models': 20},
        '50% Coverage\n0-week': {'rank': 8, 'total_models': 20},
        '50% Coverage\n1-week': {'rank': 7, 'total_models': 20},
        '95% Coverage\n0-week': {'rank': 4, 'total_models': 20},
        '95% Coverage\n1-week': {'rank': 5, 'total_models': 20},
    }

    output_path = 'cards/umass-flusion-spider.png'

    generate_spider_plot(
        model_name='UMass-flusion',
        metrics_data=metrics_data,
        output_path=output_path
    )

    print(f"Sample spider plot generated: {output_path}")
    return output_path


if __name__ == '__main__':
    generate_sample_spider_plot()
